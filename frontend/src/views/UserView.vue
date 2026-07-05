<!-- <template>
    <div> 
        <div v-if="!isLoggedIn">

            <UserLogin v-if="!showRegister" @Register-link-clicked="showRegister = true"  @logged-in="handleLogin"/>
            <UserRegister v-else @registered="handleRegister" @login-link-clicked="showRegister = false"/>
        
        </div>
        <div v-else>

            <UserDash  />

        </div>

    </div>
    
</template>

<script>
    import UserRegister from '../components/UserRegister.vue'
    import UserLogin from '../components/Login.vue'
    import UserDash from '../components/UserDash.vue'

    export default {
        name: 'UserView',

        components: {
            UserRegister,
            UserLogin,
            UserDash
        },

        data () {
            return {
                showRegister: false,    //starts with the login page
                isLoggedIn: false,
                user: null
            }
        },

        methods: {
            handleRegister (user) {
                console.log('User registered', user);
                this.showRegister = false;
            },
            handleLogin (user) {
                console.log('User logged in', user);
                
                this.isLoggedIn = true;
                this.user = user;
            }
            
        }
    }
</script> -->

<template>
    <UserDash />
</template>

<script>
import UserDash from "../components/trekker/UserDash.vue";

export default {
    name: "UserView",

    components: {
        UserDash
    }
};
</script>