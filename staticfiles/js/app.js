let items = document.querySelectorAll('.slider .list .item');
let next = document.getElementById('next');
let prev = document.getElementById('prev');
let thumbnails = document.querySelectorAll('.thumbnail .item');
let buybtns = document.querySelectorAll('.buybtn');

items.forEach((item, index) => {
  if (index > 0) {
    item.classList.remove('active');
  }
});
thumbnails.forEach((item, index) => {
  if (index > 0) {
    item.classList.remove('active');
  }
});
// config param
let countItem = items.length;
let itemActive = 0;
// event next click
next.onclick = function () {
  itemActive = itemActive + 1;
  if (itemActive >= countItem) {
    itemActive = 0;
  }
  showSlider();
};
//event prev click
prev.onclick = function () {
  itemActive = itemActive - 1;
  if (itemActive < 0) {
    itemActive = countItem - 1;
  }
  showSlider();
};
// auto run slider
//let refreshInterval = setInterval(() => {
//    next.click();
//}, 5000)
function showSlider() {
  // remove item active old
  let itemActiveOld = document.querySelector('.slider .list .item.active');
  let thumbnailActiveOld = document.querySelector('.thumbnail .item.active');
  itemActiveOld.classList.remove('active');
  thumbnailActiveOld.classList.remove('active');

  // active new item
  items[itemActive].classList.add('active');
  thumbnails[itemActive].classList.add('active');

  // clear auto time run slider
  //  clearInterval(refreshInterval);
  //  refreshInterval = setInterval(() => {
  //    next.click();
  //  }, 5000);
}

// click thumbnail
thumbnails.forEach((thumbnail, index) => {
  thumbnail.addEventListener('click', () => {
    itemActive = index;
    showSlider();
  });
});

// window.onscroll = function () {
//   myFunction();
// };

// var header = document.getElementById('myHeader');
// var sticky = header.offsetTop;

// function myFunction() {
//   if (window.pageYOffset > sticky) {
//     header.classList.add('sticky');
//   } else {
//     header.classList.remove('sticky');
//   }
// }

const block = document.querySelector('.thumbnail'); // Выбираем блок по селектору
const item = block.querySelectorAll('.item'); // Выбираем все элементы с классом "item" внутри блока
const count = item.length; // Получаем количество элементов

const slider = document.querySelector('.slider');
let ind = count / 6;

function updateSliderPosition() {
  if (!Number.isInteger(ind)) {
    slider.style.marginBottom = parseInt(ind) * block.offsetHeight - 25 * parseInt(ind) + 'px';
    console.log(parseInt(ind));
  } else {
    slider.style.marginBottom = parseInt(ind) * block.offsetHeight - 25 * parseInt(ind) + 'px';
  }
}

window.onload = updateSliderPosition;
updateSliderPosition();
console.log(block.offsetHeight, slider.style.marginBottom);
