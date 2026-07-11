
<template>
    <div class = "container-fluid bg-light vh-100">
        <div>
            <div class = "row">
                <nav class="navbar navbar-expand-lg bg-light border-bottom px-2">
                    <div class="container-fluid">
                        <span class = "navbar-brand">
                           <h1 class = "mt-2 fw-semibold display-4">
                        Trek Management
                    </h1>
                    <p class = "fw-semibold text-muted ms-1">
                        Manage your treks and schedules
                    </p>
                        </span>
                        <div class = "d-flex align-items-end">
                            <button @click = "emitCreateTrek" class = "btn btn-lg btn-success p-3 px-5 fw-semibold">
                                Create Trek
                            </button>
                        </div>
                    </div>
                </nav>
                
            </div>
            <div>
                <div>
                    <div class = "card shadow-sm border border-0 mt-4 p-3">
                        <div class = "card-header bg-white border-bottom ">
                            <h4 class = "fw-semibold">
                                Trek Route
                            </h4>
                            <p class = "text-muted fw-semibold">
                                Trek routes you have created but not scheduled
                            </p>
                        </div>
                        <div class = "card-body">
                           <table class = "table table-hover table-striped">
                                <thead>
                                    <tr>
                                        <th>
                                            Name
                                        </th>
                                        <th>
                                            Location
                                        </th>
                                        <th>
                                            Duration
                                        </th>
                                        <th>
                                            Difficulty
                                        </th>
                                        <th class = "text-center">
                                            Action
                                        </th>
                                    </tr>
                                </thead>
                                <tbody >
                                    <tr v-for = "new_route in new_trek_routes" :key = "new_route.trek_id">
                                        <td>
                                            {{ new_route.route_name }}
                                        </td>
                                        <td>
                                            {{ new_route.location }}
                                        </td>
                                        <td>
                                            {{ new_route.days_on_trail }}
                                        </td>
                                        <td>
                                            {{ new_route.difficulty }}
                                        </td>
                                        <td class = "text-center">
                                            <button @click = "emitScheduleTrek(new_route)" class = "btn btn-sm px-4 btn btn-outline-success">
                                                Schedule Trek
                                            </button>
                                        </td>
                                    </tr>
                            
                                
                                </tbody>
                           </table>
                            
                            
                        </div>
                    </div>


                    <div class = "card shadow-sm border border-0 mt-4 p-3">
                        <div class = "card-header bg-white border-bottom ">
                            <h4 class = "fw-semibold">
                                Scheduled Treks
                            </h4>
                            <p class = "text-muted fw-semibold">
                                Treks that are Scheduled and Publised
                            </p>
                        </div>
                        <div class = "card-body">
                           <table class = "table table-hover table-striped">
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
                                            Available Slots
                                        </th>
                                        <th>
                                            Status
                                        </th>
                                        <th>
                                            Price
                                        </th>
                                        <th class = "text-center">
                                            Action
                                        </th>
                                    </tr>
                                </thead>
                                <tbody >
                                    <tr v-for = "new_scheduled_trek in new_scheduled_treks" :key = "new_scheduled_trek.trek_id">
                                        <td>
                                            {{ new_scheduled_trek.trek_name }}
                                        </td>
                                        <td>
                                            {{ new_scheduled_trek.start_date }}
                                        </td>
                                        <td>
                                            {{ new_scheduled_trek.end_date }}
                                        </td>
                                        <td>
                                            {{ new_scheduled_trek.available_slots }}
                                        </td>
                                        <td>
                                            {{ new_scheduled_trek.status }}
                                        </td>
                                        <td>
                                            {{ new_scheduled_trek.price }}
                                        </td>
                                        <td class = "text-center">
                                            <button @click = "emitManageScheduledTrek(new_scheduled_trek)" class = "btn btn-sm px-4 btn btn-outline-success">
                                                Manage Trek
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


import axios from "axios";

import ScheduleTrek from "@/components/admin/ScheduleTrek.vue";

import ManageScheduledTrek from "@/components/admin/ManageScheduledTrek.vue";

export default {
    name: "TrekManagement",

    components: {
      ScheduleTrek  ,

      ManageScheduledTrek
    },

    data() {
        return {
            new_trek_routes : [],
            new_scheduled_treks : []
        }
    },

    mounted() {
        this.fetchTrekRoutes();
        this.fetchScheduledTrekRoutes();
    },

    methods : {
        goBack() {
            this.$emit("go-back");
        },

        emitCreateTrek() {
            this.$emit('show-trek');
        },


        async fetchTrekRoutes() {

            try {
                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/all_treks", {
                    headers : {
                        "Authorization" : `Bearer ${token}`
                    }
                });
                if (res.status === 200) {
                    this.new_trek_routes = res.data.trek_routes;
                    console.log(this.new_trek_routes);
                }
            } catch (error) {
                console.error("Error fetching trek routes:", error);
            }
            
        },



        async fetchScheduledTrekRoutes() {

            try {
                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/scheduled_treks", {
                    headers : {
                        "Authorization" : `Bearer ${token}`
                    }
                });
                if (res.status === 200) {
                    this.new_scheduled_treks = res.data.treks;
                    console.log(" Scheduled Trek routes loaded:", this.new_scheduled_treks);
                }
            } catch (error) {
                console.error("Error fetching trek routes:", error);
            }   

        },

        
        emitScheduleTrek(route) {
            this.$emit('schedule-trek', {
                route_id : route.trek_id,
                trek_name : route.route_name
            });
        },

        emitManageScheduledTrek(trek) {
            this.$emit('manage-scheduled-trek', trek);
        }

    }
}
</script>
        
