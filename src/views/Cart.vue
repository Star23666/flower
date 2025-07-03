<template>
  <div class="container">
    <h2>Cart</h2>
    <ul>
      <li v-for="item in cart" :key="item.id">
        {{ item.name }} - {{ item.quantity }} x ${{ item.price }}
      </li>
    </ul>
    <button class="btn btn-success" @click="placeOrder">Place Order</button>
  </div>
</template>

<script>
export default {
  name: 'ShoppingCart', // Changed from 'Cart'
  computed: {
    cart() {
      return this.$store.state.cart;
    }
  },
  methods: {
    placeOrder() {
      this.$store.dispatch('createOrder');
    }
  }
};
</script>