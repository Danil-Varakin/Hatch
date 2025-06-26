function switchMode(type, mode) {
    const autoButton = document.getElementById(`${type}-auto`);
    const manualButton = document.getElementById(`${type}-manual`);
    const fileInput = document.getElementById(`${type}-file`);
    const manualText = document.getElementById(`${type}-manual-text`);

    if (mode === 'auto') {
        fileInput.style.display = 'block';
        manualText.style.display = 'none';
        autoButton.classList.add('active');
        manualButton.classList.remove('active');
    } else {
        fileInput.style.display = 'none';
        manualText.style.display = 'block';
        autoButton.classList.remove('active');
        manualButton.classList.add('active');
    }
}

function checkInput(blockType) {
    const fileInput = document.getElementById(`${blockType}-file-input`);
    const textArea = document.getElementById(`${blockType}-text`);
    const fileDisplay = document.getElementById(`${blockType}-file`).style.display;

    if (fileDisplay === 'block') {
        if (fileInput.files.length === 0) {
            alert(`Пожалуйста, загрузите файл для ${blockType}`);
            return false;
        }
        return 'file';
    } else {
        if (textArea.value.trim() === '') {
            alert(`Пожалуйста, введите текст для ${blockType}`);
            return false;
        }
        return 'text';
    }
}

function DetectProgrammingLanguage(FileNameSourceCode) {
    const extensions = {
        '.py': 'python',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.js': 'javascript',
        '.rb': 'ruby',
        '.ts': 'typescript',
        '.go': 'go',
        '.rs': 'rust'
    };
    const ext = '.' + FileNameSourceCode.split('.').pop();
    return extensions[ext] || 'Неизвестный язык';
}

function apply() {
    let matchContent = '';
    let sourceContent = '';
    let matchType = '';
    let sourceType = '';
    let sourceLanguage = '';

    const matchInputType = checkInput('Match');
    const matchFileInput = document.getElementById('Match-file-input');
    const matchTextArea = document.getElementById('Match-text');

    if (matchInputType === 'file') {
        matchContent = matchFileInput.files[0].name;
        matchType = 'file';
    } else {
        matchContent = matchTextArea.value.trim();
        matchType = 'text';
    }

    const sourceInputType = checkInput('SourceCode');
    const sourceFileInput = document.getElementById('SourceCode-file-input');
    const sourceTextArea = document.getElementById('SourceCode-text');
    const sourceSelect = document.getElementById('SourceCode-manual-select');

    if (sourceInputType === 'file') {
        sourceContent = sourceFileInput.files[0].name;
        sourceType = 'file';
        sourceLanguage = DetectProgrammingLanguage(sourceContent);
    } else {
        sourceContent = sourceTextArea.value.trim();
        sourceType = 'text';
        sourceLanguage = sourceSelect.value;
    }

    const ListOfCodeAndInstruction = [matchContent, matchType, sourceContent, sourceType, sourceLanguage];

    if (window.pywebview && window.pywebview.api && window.pywebview.api.ProcessInputData) {
        window.pywebview.api.ProcessInputData(ListOfCodeAndInstruction)
    }
}