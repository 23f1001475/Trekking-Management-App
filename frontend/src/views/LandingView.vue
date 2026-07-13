
<template>
  <div style="background-image: url('src/styles/images/LandingPage.png'); background-size: cover; background-position: center center">

    <div class="text-white fw-bold fs-1 p-5">
    SummitGo
    </div>
    
      
    
    <div class="ms-2 row align-items-center" style = "height: 87vh"> <!-- vh : viewport height for full browser screen css : height : 100% / 100vh -->

      <div class="ps-5">
            <h1 class="text-white fw-bold display-3">

              Let's Go Hiking

            </h1>

            <p class="text-white">

                Start your next trekking adventure

            </p>

            <button class="btn btn-light btn-lg mt-3" @click="$router.push('/login')">
        
              Start Your Hike

            </button>  
              
        </div>

    </div>
  </div>
  


      

  

</template>

<script>
export default {
  name: "LandingView"
}
</script>
