const updateBtns = document.getElementsByClassName('update-cart'); // home.html & product.html
const updateItems = document.getElementsByClassName('update-item'); // cart.html

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function () {
    let productId = this.dataset.product
    let action = this.dataset.action
    let parent = this.previousElementSibling.children
    let option = parent[1].options[parent[1].selectedIndex].value
    let values = option.split(' ');
    let packet = parseInt(values[0])
    let price = parseFloat(values[1])
    updateUserOrderHome(productId, action, packet, price)
  })
}

for (i = 0; i < updateItems.length; i++) {
  updateItems[i].addEventListener('click', function () {
    let productId = this.dataset.product
    let action = this.dataset.action
    let price = this.dataset.price;
    let packet = this.dataset.packet;
    updateUserOrderCart(productId, action, packet, price)
  })
}

async function updateUserOrderCart(productId, action, packet, price) {
  const url = "/update_item/";

  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
      packet: packet,
      price: price,
    }),
  });
  let data = await response.json();
  changeHTMLCart(productId, action, packet, price, data['cart_items'], data['cart_total'])
}

async function updateUserOrderHome(productId, action, packet, price) {
  const url = "/update_item/";

  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
      packet: packet,
      price: price,
    }),
  });
  let data = await response.json();
  changeHTMLHome(productId, action, packet, price, data['cart_items'], data['cart_total'])
}

function changeHTMLCart(productId, action, packet, price, totalItems, totalPrice) {
  // Τα συνολικά τεμάχια που φαίνονται στο μενού
  let shoppingCartItems = document.querySelector('.shopping-cart-items');
  // Τα συνολικά τεμάχια που φαίνονται στην σύνοψη της κάρτας
  let cartQuantity = document.querySelector('.cart-quantity');
  // Η συνολική τιμή που φαίνεται στην σύνοψη της κάρτας
  let cartTotal = document.querySelector('.cart-total');

  // Update individual product quantity
  const quantity_tag = (parseInt(`${productId}${packet}${price}`)).toString();
  let productQuantity = document.getElementById(quantity_tag);
  let quantity = parseInt(productQuantity.textContent);
  if (action==='add') {
    quantity+=1;
  } else if (action==='remove') {
    quantity-=1;
  }
  productQuantity.textContent=quantity;

  // Update individual product total price
  price = parseInt(price);
  const price_tag = (parseInt(`${price}${packet}${productId}`)).toString();
  let productTotalPrice = document.getElementById(price_tag);
  let totalPriceProduct = parseInt(productTotalPrice.textContent);
  if (action==='add') {
    totalPriceProduct+=price;
  } else if (action==='remove') {
    totalPriceProduct-=price;
  }
  productTotalPrice.textContent=totalPriceProduct.toFixed(2);

  // Ανανέωση των τεμαχίων στο μενού
  shoppingCartItems.textContent = totalItems;
  // Ανανέωση των τεμαχίων στην σύνοψη της κάρτας
  cartQuantity.textContent = totalItems;
  // Ανανέωση του συνολικού ποσού στην σύνοψη της κάρτας
  cartTotal.textContent = totalPrice;

  // Αν τα τεμάχια στο μενού είναι 0 ή κάποια ποσότητα γίνει 0 ή αν πατηθεί το delete, ανανέωσε τη σελίδα
  if (parseInt(shoppingCartItems.textContent) <= 0 || quantity <= 0 || action === 'delete') {
    location.reload();
  }
}

function changeHTMLHome(productId, action, packet, price, totalItems, totalPrice) {
  // Τα συνολικά τεμάχια που φαίνονται στο μενού
  let shoppingCartItems = document.querySelector('.shopping-cart-items');

  // Ανανέωση των τεμαχίων στο μενού
  shoppingCartItems.textContent = totalItems;
}
