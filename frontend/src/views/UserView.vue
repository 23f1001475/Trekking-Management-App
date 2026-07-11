
<template>
    <TrekkerDash @show-profile = "handleShowProfile"  @show-history = "handleShowHistory"  @book-now-trek = "handleBookNowTrek" v-if="!showProfile  && !showHistory && !showBookNowTrek" />
    <TrekHistory  @show-history = "handleShowHistory"   @go-back = "handleBackToDashboard" v-if="showHistory" />
    <TrekkerProfile @show-profile = "handleShowProfile" @go-back = "handleBackToDashboard"  v-if="showProfile" />

    <BookTrek v-if="showBookNowTrek" :trek-id="selectedTrekID" @back-to-dashboard="handleBackToDashboard"/>
</template>

<script>
import TrekkerDash from "../components/trekker/TrekkerDash.vue";

import TrekkerProfile from "../components/trekker/TrekkerProfile.vue";
import TrekHistory from "../components/trekker/TrekHistory.vue"; 
import BookTrek from "../components/trekker/BookTrek.vue";


export default {
    name: "UserView",

    data() {
        return {
            showProfile: false,
            showHistory: false,
            showBookNowTrek: false,
            selectedTrekID: null

        };
    },

    components: {
        TrekkerDash,
        TrekkerProfile,
        TrekHistory,
        BookTrek
    },

    methods : {

        handleShowProfile() {
            this.showProfile = true;
            this.showHistory = false;
            this.showBookNowTrek = false;
            this.selectedTrekID = null
        },

        handleShowHistory() {
            this.showHistory = true;
            this.showProfile = false;
            this.showBookNowTrek = false;
            this.selectedTrekID = null
        },
        handleBookNowTrek(trekId) {
            this.showBookNowTrek = true;
            this.showHistory = false;
            this.showProfile = false;

            this.selectedTrekID = trekId;
        },

        handleBackToDashboard () {
            this.showProfile = false;
            this.showHistory = false;
            this.showBookNowTrek = false;
        }
    }
};
</script>
