const testimonyButton = document.getElementById('testimonyButton');
const closeModalButton = document.getElementById('closeModalButton');
const modal = document.getElementById('testimonyModal');

testimonyButton.onclick = (() => {
    modal.classList.remove('hidden');
});

closeModalButton.onclick = (() => {
    modal.classList.add('hidden');
});
