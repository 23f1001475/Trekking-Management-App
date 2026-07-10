<template>
    <div class = "container-fluid bg-light vh-100">
            
        <div>
            <div class = "row">

                <nav class="navbar navbar-expand-lg bg-white border-botton shadow-sm">

                    <div class = "container-fluid">
                        <span class = "navbar-brand fw-semibold">
                            
                            Welcome {{ staff_name }}
                        </span>
                            
                        
                        <div class = "d-flex align-items-center">

                            <input v-model = "searchText" class = "form-control me-3"  type = "search" placeholder = "Search" style= "width: 220px" />

                            <button @click = "logout()" class = "btn btn-secondary">
                                Logout
                            </button>

                        </div>

                    </div>

                </nav>
            </div>
                
            <div class = "container shadow-sm bg-white  mt-5 p-3 rounded-3">
                <div class = "row text-center">

                    <div class = "d-flex justify-content-center gap-5">

                        <div class = "col-4">

                            <div class = "card shadow-sm mt-3 mb-3 rounded-4">

                               <div class = "card-header fw-bold p-3 rounded-top-4">
                                   
                                       Total Assigned Treks
                                   
                               </div>
                               <div class = "card-body fw-semibold fs-2">
                                    
                                        {{ total_assigned_treks }}

                               </div>
                            </div>
                        </div>
                        
                        <div class = "col-4">
                            <div class = "card shadow-sm mt-3 mb-3 rounded-4">
                               <div class = "card-header fw-bold p-3 rounded-top-4">
                                   
                                       Total Completed Treks
                                   
                               </div>
                               <div class = "card-body fw-semibold fs-2">
                                   
                                        {{ total_completed_treks }}
                                        
                               </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class = "container card shadow-sm border-0 bg-white text-center mt-5  rounded-3">

                <div class="row">
                    <div class = "card-header fw-semibold">
                        Assigned Treks
                    </div>
                    <div class = "card-body p-4">
                        <div class = "table-responsive  rounded-4 border">
                        <table class = "table table-hover table-striped table-bordered"  style = "border-radius: 20px;">
                            <thead>
                                <tr>
                                    <th>
                                        Trek Name
                                    </th>
                                    <th>
                                        Start Date
                                    </th>
                                    <th>
                                        End Date
                                    </th>
                                    <th> 
                                        Status
                                    </th>
                                    <th>
                                        Total Participants
                                    </th>
                                    <th>
                                        Actions
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for = "assigned_trek in filteredAssignedTrek" :key = "assigned_trek.trek_id">
                                    <td>
                                        {{ assigned_trek.route_name }}

                                    </td>
                                    <td>
                                        
                                        {{ assigned_trek.start_date }}
                                    </td>
                                    <td>
                                        {{ assigned_trek.end_date }}
                                    </td>
                                    <td>
                                        {{ assigned_trek.status }}
                                    </td>
                                    <td>
                                        {{ assigned_trek.registered_trekkers }}
                                    </td>
                                    <td>

                                        <button  @click = "ShowAssignedTrek(assigned_trek.trek_id)" class = "btn btn-sm btn-primary">
                                            View
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        </div>
                    </div>
                </div>
                
            </div>
                
            

        </div>

    </div>

    
</template>

<script>
import TrekStatusManagement from '@/components/trek_staff/TrekStatusManagement.vue'
import AssignedTrek from '@/components/trek_staff/AssignedTrek.vue'
import ParticipantList from '@/components/trek_staff/ParticipantList.vue';


import axios from "axios";

export default {
    name: 'TrekStaffDash',

    data() {
        return {

            staff_name : "",
            assigned_treks : [],
            searchText : "",
            total_assigned_treks : 0,
            total_completed_treks : 0,
        }
    },

    components: {

        AssignedTrek,
        ParticipantList,
        TrekStatusManagement
    },

    computed : {

        filteredAssignedTrek() {

            const search = this.searchText.trim().toLowerCase();

            if (!search) {

                return this.assigned_treks;

            }
            return this.assigned_treks.filter((assigned_trek) => {
                
                return assigned_trek.trek_name.toLowerCase().includes(search);

            });
        }

    },


    mounted(){

        this.fetchAssignedTrek();
    },

    methods : {

        async fetchAssignedTrek() {

            try {
                const token = localStorage.getItem("token");

                const res = await axios.get(`http://127.0.0.1:5000/api/staff/dashboard`, { 
                    
                    headers : {
                        "Authorization" : `Bearer ${token}`
                    }
                });

                if (res.status === 200) {

                    console.log(res.data);
                    this.assigned_treks = res.data.assigned_treks;
                    this.staff_name = res.data.staff_name;
                    this.total_completed_treks = res.data.total_completed_treks;
                    this.total_assigned_treks = res.data.total_assigned_treks;
                }

            } catch (error) {

                console.error("Error fetching assigned treks:", error);

                }

        },

        logout() {
            localStorage.removeItem("token");
            this.$router.push("/login");
        },

        goBack() {
            this.$emit("go-back")
        },


        ShowAssignedTrek(trek_id) {

            this.$emit("show-assigned-trek", trek_id);
        }
    }
}
</script>