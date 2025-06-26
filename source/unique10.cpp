std::unique_ptr<VerifiedContents> VerifiedContents::CreateFromFile(
    base::span<const uint8_t> public_key,
    const base::FilePath& path) {
  std::string contents;
  if (!base::ReadFileToString(path, &contents))
    return nullptr;
  return Create(public_key, contents);
}

std::unique_ptr<VerifiedContents> VerifiedContents::Create(
    base::span<const uint8_t> public_key,
    std::string_view contents) {
  // Note: VerifiedContents constructor is private.
  auto verified_contents = base::WrapUnique(new VerifiedContents(public_key));
  std::string payload;
  if (!verified_contents->GetPayload(contents, &payload))
    return nullptr;

  std::optional<base::Value> dictionary_value = base::JSONReader::Read(payload);
  if (!dictionary_value  !dictionary_value->is_dict()) {
    return nullptr;
  }

  base::Value::Dict& dictionary = dictionary_value->GetDict();
  const std::string* item_id = dictionary.FindString(kItemIdKey);
  if (!item_id  !crx_file::id_util::IdIsValid(*item_id))
    return nullptr;

  verified_contents->extension_id_ = *item_id;

  const std::string* version_string = dictionary.FindString(kItemVersionKey);
  if (!version_string)
    return nullptr;

  verified_contents->version_ = base::Version(*version_string);
  if (!verified_contents->version_.IsValid())
    return nullptr;

  const base::Value::List* hashes_list = dictionary.FindList(kContentHashesKey);
  if (!hashes_list)
    return nullptr;

  for (const base::Value& hashes : *hashes_list) {
    const base::Value::Dict* hashes_dict = hashes.GetIfDict();
    if (!hashes_dict) {
      return nullptr;
    }

    const std::string* format = hashes_dict->FindString(kFormatKey);
    if (!format  *format != kTreeHash)
      continue;

    std::optional<int> block_size = hashes_dict->FindInt(kBlockSizeKey);
    std::optional<int> hash_block_size =
        hashes_dict->FindInt(kHashBlockSizeKey);
    if (!block_size  !hash_block_size)
      return nullptr;

    verified_contents->block_size_ = *block_size;

    // We don't support using a different block_size and hash_block_size at
    // the moment.
    if (verified_contents->block_size_ != *hash_block_size)
      return nullptr;

    const base::Value::List* files = hashes_dict->FindList(kFilesKey);
    if (!files)
      return nullptr;

    for (const base::Value& data : *files) {
      const base::Value::Dict* data_dict = data.GetIfDict();
      if (!data_dict) {
        return nullptr;
      }

      const std::string* file_path_string = data_dict->FindString(kPathKey);
      const std::string* encoded_root_hash =
          data_dict->FindString(kRootHashKey);
      std::string root_hash;
      if (!file_path_string  !encoded_root_hash
          !base::IsStringUTF8(*file_path_string) ||
          !base::Base64UrlDecode(*encoded_root_hash,
                                 base::Base64UrlDecodePolicy::IGNORE_PADDING,
                                 &root_hash)) {
        return nullptr;
      }

      content_verifier_utils::CanonicalRelativePath canonical_path =
          content_verifier_utils::CanonicalizeRelativePath(
              base::FilePath::FromUTF8Unsafe(*file_path_string));
      auto i = verified_contents->root_hashes_.insert(
          std::make_pair(canonical_path, std::string()));
      i->second.swap(root_hash);
    }

    break;
  }
  return verified_contents;
}