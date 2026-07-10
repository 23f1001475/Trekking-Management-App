<template>
    <div class = "container-fluid bg-light vh-min-100" >
        <div>
            <div class = "row">
                <nav class = "navbar navbar-extended bg-white border-bottom shadow-sm px-3">
                    <div class = "container-fluid">
                        <span class = "navbar-brand">
                            <div class = "fw-semibold display-4">
                                Assigned Trek
                            </div>
                        </span>

                        <div class = "d-flex align-items-center">
                            <button  @click = "goBack()" class = "btn btn-secondary">

                                Go Back

                            </button>

                        </div>
                    </div>
                </nav>

            </div>


            <div class = "container mt-5" style = "width: 900px;">

                <div class="card border" >
                    <div class = "card-header border-0 shadow-sm text-center">
                        <strong class = "fw-bold display-6">
                            {{ trek_data.route_name }}
                        </strong>
                    </div>

                    <img :src="trek_data.image" class="card-img-top" alt="...">
                        
                    <div class="card-body">

                            <div class = "shadow-sm p-3">

                                <div class = "row ">

                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Description :
                                        </p>
                                    </div>
                                    <div class="col-9">

                                        <p class = "fw-semibold">
                                            {{ trek_data.description }}
                                        </p>

                                    </div>

                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Trek Name :
                                        </p>
                                    </div>
                                    <div class="col-9">

                                        <p class = "fw-semibold">
                                            {{ trek_data.route_name }}
                                        </p>

                                    </div>

                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Next Departure :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.start_date }}
                                        </p>
                                    </div>

                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            End Date :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.end_date }}
                                        </p>
                                    </div>

                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Location :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.location }}
                                        </p>
                                    </div>
                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Altitude :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.altitude }}
                                        </p>
                                    </div>

                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Total Participants :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.registered_trekkers }}
                                        </p>
                                    </div>
                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Difficulty :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.difficulty }}
                                        </p>
                                    </div>

                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Assigned Staffs :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.assigned_staffs }}
                                        </p>
                                    </div>
                                    
                                    <div class = "col-3">
                                        <p class = "fw-semibold">
                                            Status :
                                        </p>
                                    </div>
                                    <div class="col-9">
                                        <p class = "fw-semibold">
                                            {{ trek_data.status }}
                                        </p>
                                    </div>
                                    
            
                                </div>
                                
                            </div>
                        </div>

                        <div class = "card-footer">
                            <div class = "d-flex justify-content-center">
                            <button @click = "ShowParticipantList()" class = "btn btn-primary me-5">
                                Participant List
                            </button>
                            <button  @click = "ShowTrekStatusManagement()" class = "btn btn-primary">
                                Manage Trek
                            </button>
                            </div>
                        </div>
                </div>
            </div>
        </div>
    </div>

    <div class="bg-light" style = "height : 200px">
        

       
    </div>

</template> 

<script>


import axios from "axios";
export default {
    name : "AssignedTrek",

    data () {
        return {
            trek_data : {}
        }
    },


    props : {
        trekId : [Number]
    },


    mounted() {

        this.fetchTrekDetails();
    },

    methods : {

        async fetchTrekDetails () {

            try{
                const token = localStorage.getItem("token");

                const res = await axios.get(`http://127.0.0.1:5000/api/staff/treks/${this.trekId}`, {

                    headers : {
                        "Authorization" : `Bearer ${token}`
                    }
                });
                if (res.status === 200) {

                    this.trek_data = res.data;
                }

            } catch (error) {

                console.error("Error fetching trek details:", error);
                alert("Failed to load trek details.");
                
            }
        },

        ShowParticipantList() {

            this.$emit("show-participants", this.trekId)
        },

        ShowTrekStatusManagement() {

            this.$emit("show-manage-trek-status", this.trekId)
        },




        goBack() {
            this.$emit("go-back")
        }
    }
}
</script>
