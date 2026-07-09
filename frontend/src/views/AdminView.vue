<template>
    <div>
        <div>

          <AdminDash @create-staff="handleCreateStaff" @show-trekker="handleShowTrekker" @show-staff="handleShowStaff"  @show-trek="handleShowTrek"  @manage-trek="handleShowTrekManage" @schedule-trek="handleScheduleTrek"  @manage-scheduled-trek="handleManageScheduledTrek"   @show-booking = "handleShowBooking"     @show-reports = "handleShowReports"  v-if="!showTrekker && !showStaff && !showCreateStaff  && !showCreateTrek  && !showManageTrek  && !showScheduleTrek  && !showManageScheduledTrek  && !showBookingManagement   && !showReports" />

          <!-- <TrekkerManagement v-if="showTrekker" /> -->
          <TrekkerManagement @go-back="showTrekker = false" v-if="showTrekker" />


          <StaffManagement @show-trekker = "handleShowTrekker" @create-staff = "handleCreateStaff" @staff-created = "showCreateStaff = false" @go-back="showStaff = false" v-if="showStaff" />

          <CreateStaff @show-staff = "handleShowStaff" @go-back = "showCreateStaff = false"   @staff-created = "handleStaffCreated" v-if="showCreateStaff" />

          <CreateTrek @show-trek = "handleShowTrek" @go-back = "showCreateTrek = false" @manage-trek = "handleShowTrekManage" @trek-created = "handleTrekCreated" v-if = "showCreateTrek" />

          <TrekManagement @show-trek = "handleShowTrek" @manage-trek = "handleShowTrekManage" @schedule-trek = "handleScheduleTrek"  @manage-scheduled-trek = "handleManageScheduledTrek"  @go-back = "showManageTrek = false"   v-if = "showManageTrek" />

          <ScheduleTrek :route-id = "selectedRouteID" :trek-name = "selectedTrekName" @manage-trek = "handleShowTrekManage"    @go-back = "showScheduleTrek = false; showManageTrek = true" @trek-scheduled="handleTrekScheduled" v-if = "showScheduleTrek" />

          <ManageScheduledTrek :trek-id = "selectedScheduledTrekID" @go-back = "showManageScheduledTrek = false" v-if = "showManageScheduledTrek" />

          <BookingManagement @go-back = "showBookingManagement = false" v-if = "showBookingManagement" />

          <Reports @go-back = "showReports = false" v-if = "showReports" />
        </div>

  </div>

</template>

<script>
import TrekkerManagement from "@/components/admin/TrekkerManagement.vue";
import StaffManagement from "@/components/admin/StaffManagement.vue";
import AdminDash from "../components/admin/AdminDash.vue";
import CreateStaff from "@/components/admin/CreateStaff.vue";
import CreateTrek from "@/components/admin/CreateTrek.vue"; 
import TrekManagement from "@/components/admin/TrekManagement.vue";
import ScheduleTrek from "@/components/admin/ScheduleTrek.vue";
import ManageScheduledTrek from "@/components/admin/ManageScheduledTrek.vue";
import BookingManagement from "@/components/admin/BookingManagement.vue";
import Reports from "@/components/admin/Reports.vue";


export default {
    name: "AdminView",

    components: {
        AdminDash,

        TrekkerManagement,

        StaffManagement,

        CreateStaff,

        CreateTrek,

        TrekManagement,

        ScheduleTrek,

        ManageScheduledTrek,

        BookingManagement,

        Reports

    },


    data () {
        return {
            showTrekker: false,
            showStaff: false,
            showCreateStaff: false,
            showCreateTrek: false,
            showManageTrek: false,
            showScheduleTrek: false,
            showManageScheduledTrek: false,
            showBookingManagement: false,
            selectedRouteID : null,
            selectedTrekName: "",
            selectedScheduledTrekID: null,
            showReports: false
        }
    },

    methods : {
        handleShowTrekker() {
            this.showTrekker = true;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showReports = false
        },

        handleShowStaff() {
            this.showStaff = true;
            this.showTrekker = false;
            this.showCreateStaff = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showReports = false
        },


        handleCreateStaff() {
            this.showCreateStaff = true;
            this.showStaff = false;
            this.showTrekker = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showReports = false
            

        },

        handleStaffCreated() {
            this.showCreateStaff = false;
            this.showStaff = true;
            this.showTrekker = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showReports = false
        },


        handleShowTrek() {
            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showCreateTrek = true;
            this.showManageTrek = false;
            this.showReports = false
        },

        handleTrekCreated() {
            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showCreateTrek = false;
            this.showManageTrek = true;
            this.showReports = false    
        },

        handleShowTrekManage() {
            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showManageTrek = true;
            this.showCreateTrek = false;
            this.showReports = false

        },

        handleScheduleTrek(route) {
            this.selectedRouteID = route.route_id;
            this.selectedTrekName = route.trek_name;

            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showManageScheduledTrek = false;
            this.showScheduleTrek = true;

            this.showReports = false
        },

        handleManageScheduledTrek(trek) {
            if (!trek) {
                this.handleShowTrekManage();
                return;
            }

            this.selectedScheduledTrekID = trek.trek_id;

            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showScheduleTrek = false
            this.showManageScheduledTrek = true,
            this.showReports = false
        },

        handleTrekScheduled (scheduledTrek) {
            this.selectedScheduledTrekID = scheduledTrek?.trek_id || scheduledTrek?.scheduled_trek_id || scheduledTrek?.trek?.trek_id || null;

            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showManageTrek = !this.selectedScheduledTrekID;
            this.showCreateTrek = false;
            this.showScheduleTrek = false
            this.showManageScheduledTrek = Boolean(this.selectedScheduledTrekID);
            this.showReports = false
        },

        handleShowBooking () {
            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showScheduleTrek = false
            this.showManageScheduledTrek = false,
            this.showBookingManagement = true,
            this.showReports = false
        },

        handleShowReports () {
            this.showTrekker = false;
            this.showStaff = false;
            this.showCreateStaff = false;
            this.showManageTrek = false;
            this.showCreateTrek = false;
            this.showScheduleTrek = false
            this.showManageScheduledTrek = false,
            this.showBookingManagement = false,
            this.showReports = true
        }   
    }
};
</script>
