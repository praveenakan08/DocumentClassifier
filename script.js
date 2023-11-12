function classifyDocuments() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;

    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }

    fetch('http://localhost:5000/classify', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayFolders(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayFolders(data) {
    const foldersContainer = document.getElementById('foldersContainer');
    foldersContainer.innerHTML = '';

    for (const category in data) {
        const folderDiv = document.createElement('div');
        folderDiv.className = 'folder';

        const folderTitle = document.createElement('h3');
        folderTitle.textContent = category;
        folderDiv.appendChild(folderTitle);

        const fileList = data[category];
        if (fileList.length > 0) {
            const fileListUl = document.createElement('ul');
            fileList.forEach(fileName => {
                const listItem = document.createElement('li');
                listItem.textContent = fileName;
                fileListUl.appendChild(listItem);
            });
            folderDiv.appendChild(fileListUl);
        } else {
            const noFilesMessage = document.createElement('p');
            noFilesMessage.textContent = 'No files in this category.';
            folderDiv.appendChild(noFilesMessage);
        }

        foldersContainer.appendChild(folderDiv);
    }
}
