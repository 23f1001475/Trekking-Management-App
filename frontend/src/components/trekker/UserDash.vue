<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-white shadow-sm">
      <div class = "container">
        <a class="navbar-brand fw-bold" href="#">LOGO</a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav mx-auto">
            <li class="nav-item">
              <a class="nav-link" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Treks</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">About Us</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Contact</a>
            </li>
          </ul>

          <button class="btn btn-outline-dark me-2">Login</button>
          <button class="btn btn-dark">Register</button>
        </div>
      </div>
    </nav>
    <section class="container my-5">
      <div class="row align-items-center">

        <div class="col-md-5">
          <h1 class="fw-bold">Explore. Trek. Conquer.</h1>

          <p class="lead">
            Discover the best trekking experiences with us.
          </p>

          <button class="btn btn-dark px-4">
            Explore Treks
          </button>
        </div>

        <div class="col-md-7">
          <div class="hero-image">
            <img
              src="https://picsum.photos/700/350?mountain"
              class="img-fluid rounded"
            />
          </div>
        </div>

      </div>
    </section>

    <section class = "container mb-5">

      <div class = "d-flex justify-content-between align-items-center mb-3">
        <h3>Popular Treks</h3>

        <button class="btn btn-outline-secondary">
          View All
        </button>
      </div>

      <div class="row">

        <div
          class="col-md-3 mb-4" v-for="trek in treks" :key="trek.id">
          <div class="card h-100 shadow-sm">

            <img :src="trek.image" class="card-img-top"
            >

            <div class="card-body">

              <h5>{{ trek.name }}</h5>

              <p class="mb-1">{{ trek.location }}</p>

              <small>
                {{ trek.difficulty }}
                •
                {{ trek.duration }}
              </small>

              <h6 class="mt-2">₹ {{ trek.price }}</h6>

            </div>

          </div>
        </div>

      </div>

    </section>
  </div>
</template>

<script setup>
const treks = [
  {
    id: 1,
    name: "Kedarkantha Trek",
    location: "Uttarakhand",
    difficulty: "Easy",
    duration: "5 Days",
    price: "5,000",
    image: "https://picsum.photos/300/200?1"
  },
  {
    id: 2,
    name: "Hampta Pass",
    location: "Himachal",
    difficulty: "Moderate",
    duration: "6 Days",
    price: "6,500",
    image: "https://picsum.photos/300/200?2"
  },
  {
    id: 3,
    name: "Triund Trek",
    location: "Himachal",
    difficulty: "Easy",
    duration: "2 Days",
    price: "3,000",
    image: "https://picsum.photos/300/200?3"
  },
  {
    id: 4,
    name: "Valley of Flowers",
    location: "Uttarakhand",
    difficulty: "Moderate",
    duration: "5 Days",
    price: "5,000",
    image: "https://picsum.photos/300/200?4"
  }
];
</script>

<style scoped>
.hero-image img{
    width:100%;
    height:320px;
    object-fit:cover;
}

.card img{
    height:180px;
    object-fit:cover;
}
</style>