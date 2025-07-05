<template>
  <div class="container">
    <h2>购物</h2>
    <ul>
      <li v-for="item in cart" :key="item.id">
        {{ item.name }} - {{ item.quantity }} x ${{ item.price }}
      </li>
    </ul>
    <button class="btn btn-success" @click="placeOrder">请下单</button>
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