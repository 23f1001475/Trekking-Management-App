<template>
    <div class = "bg-light vh-100">
        <div>
            <div class = "row">
                <nav class = "navbar navbar-expand-lg bg-white border-bottom shadow-sm px-3">
                    <div class = "container-fluid">
                        <span class = "navbar-brand">
                            <div class = "fw-semibold display-3">
                                Participant List
                            </div>
                        </span>
                        <div class = "d-flex align-items-center gap-3">
                            <input v-model = "searchText"   class = "form-control w-auto" type = "search" placeholder = "Search" >
                            <button @click = "goBack()" class = "btn btn-secondary">
                                Go Back
                            </button>
                        </div>
                    </div>
                </nav>
            </div>
            
            <div class = "container mt-5">

                <div class = "card shadow-sm">

                    <div class="card-header">
                        <strong>
                            Participants of Trek
                        </strong>
                    </div>

                    <div class = "card-body">
                        <div class = "table-responsive border rounded-4">
                        <table class = "table table-responsive table-bordered table-hover table-striped"  style = "border-radius: 20px;">
                            <thead>
                                <tr>

                                    <th>
                                        Name
                                    </th>
                                    <th>
                                        Email
                                    </th>
                                    <th>
                                        Phone
                                    </th>

                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for = "participant in filteredParticipants" :key = "participant.trekker_id">

                                    <td>
                                        {{ participant.name }}
                                    </td>
                                    <td>
                                        {{ participant.email }}
                                    </td>
                                    <td>
                                        {{ participant.phone }}
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

export default {
    name : "ParticipantList"  ,

    props : {
        trekId : [Number]
    },

    data() {
        return {
            searchText : "",
            participants_list : [],
            trek_name : ""
        }
    },


    mounted(){
        this.fetchParticipants();
    },

    computed : {

        filteredParticipants() {
            

            const  search  = this.searchText.trim().toLowerCase();

            if (!search) {

                return this.participants_list;

            }
            return this.participants_list.filter((participant) => {

                return participant.name.toLowerCase().includes(search);

            });
        }

    },
    
    methods : {

        async fetchParticipants() {

            try {
                const token = localStorage.getItem("token");

                const res = await axios.get(`http://127.0.0.1:5000/api/staff/treks/${this.trekId}/participants`, {
                    
                    headers : {

                        "Authorization" : `Bearer ${token}`

                    }
                });

                if (res.status === 200) {

                    this.participants_list = res.data.participants_list;
                    this.trek_name = res.data.trek_name;
                }

            } catch (error) {

                console.error("Error fetching trek details:", error);
                alert("Failed to load trek details.");
                
            }
        },



        goBack() {
            this.$emit("go-back")
        }
    }


}

</script>
