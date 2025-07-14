function enlargeImage(img) {
  img.classList.toggle('enlarged-image');
}

const liElements = document.querySelectorAll('.enlarge-on-click');

liElements.forEach(li => {
  li.addEventListener('click', () => {
    li.classList.toggle('enlarged');
  });
});
