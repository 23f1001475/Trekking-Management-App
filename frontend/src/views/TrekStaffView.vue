<template>



    <div>

      <TrekStaffDash @show-assigned-trek = "handleShowAssigned" @show-participants = "handleShowParticipants" @show-manage-trek-status = "handleShowManageTrekStatus"    v-if = "!ShowAssignedTrek && !ShowParticipantList && !ShowTrekStatusManagement" />
      
      <AssignedTrek @go-back = "handleGoBack" @show-participants = "handleShowParticipants" @show-manage-trek-status = "handleShowManageTrekStatus"  :trek-id = "selectedTrekID" v-if="ShowAssignedTrek"/>
      
      <ParticipantList @go-back = "handleGoBack" :trek-id = "selectedTrekID" v-if = "ShowParticipantList"/>
      
      <TrekStatusManagement @go-back = "handleGoBack"  :trek-id = "selectedTrekID" v-if = "ShowTrekStatusManagement"/>

    </div>



</template>

<script>
import AssignedTrek from "@/components/trek_staff/AssignedTrek.vue";
import TrekStaffDash from "../components/trek_staff/TrekStaffDash.vue";
import ParticipantList from "@/components/trek_staff/ParticipantList.vue";
import TrekStatusManagement from "@/components/trek_staff/TrekStatusManagement.vue";

export default {
    name: "TrekStaffView",

    components: {
        TrekStaffDash,
        AssignedTrek,
        ParticipantList,
        TrekStatusManagement
    },

    data() {
      return {

        ShowAssignedTrek: false,
        ShowParticipantList: false,
        ShowTrekStatusManagement: false,

        selectedTrekID: null
      }
    },


    methods :{

        handleGoBack() {
            this.ShowAssignedTrek = false;
            this.ShowParticipantList = false;
            this.ShowTrekStatusManagement = false;
            this.selectedTrekID = null;
        },

        handleShowAssigned(trekId) {
            this.ShowAssignedTrek = true;
            this.ShowParticipantList = false;
            this.ShowTrekStatusManagement = false;
            this.selectedTrekID = trekId;
        },

        handleShowParticipants(trekId) {
            this.ShowAssignedTrek = false;
            this.ShowParticipantList = true;
            this.ShowTrekStatusManagement = false;
            this.selectedTrekID = trekId;
        },

        handleShowManageTrekStatus(trekId) {
            this.ShowAssignedTrek = false;
            this.ShowParticipantList = false;
            this.ShowTrekStatusManagement = true;
            this.selectedTrekID = trekId;

        }

    }
};
</script>
