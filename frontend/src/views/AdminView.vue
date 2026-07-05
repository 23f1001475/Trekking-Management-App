<template>
    <div>
        <div>

          <AdminDash @show-trekker="handleShowTrekker" @show-staff="handleShowStaff" v-if="!showTrekker && !showStaff" />

          <!-- <TrekkerManagement v-if="showTrekker" /> -->
          <TrekkerManagement @go-back="showTrekker = false" v-if="showTrekker" />


          <StaffManagement v-if="showStaff" />
        </div>

  </div>

</template>

<script>
import TrekkerManagement from "@/components/admin/TrekkerManagement.vue";
import StaffManagement from "@/components/admin/StaffManagement.vue";
import AdminDash from "../components/admin/AdminDash.vue";


export default {
    name: "AdminView",

    components: {
        AdminDash,

        TrekkerManagement,

        StaffManagement

    },


    data () {
        return {
            showTrekker: false,
            showStaff: false
        }
    },

    methods : {
        handleShowTrekker() {
            this.showTrekker = true;
            this.showStaff = false
        },

        handleShowStaff() {
            this.showStaff = true;
            this.showTrekker = false
        }
    }
};
</script>