<template>
    <div class = "container-fluid bg-light vh-100">

        <div class = "row">

            <nav class = "navbar navbar-expand-lg bg-white border-bottom shadow-sm px-3">
                <div class = "container-fluid">
                    <span class = "navbar-brand">
                        <div class = "fw-semibold display-3">
                            Manage Trek
                        </div>
                    </span>
                    <button @click = "goBack()" class = "btn btn-secondary">
                        Go Back
                    </button>
                </div>
            </nav>

        </div>

        <div class = "container mt-5" style = "max-width: 700px;">

            <div class = "card shadow-sm">
                <div class = "card-header fw-semibold">

                    {{ trek.route_name }}

                </div>

                <div class = "card-body">
                    <div class = "mb-3">

                        <label class = "form-label">
                            Available Slots
                        </label>
                        <input v-model.number = "form.available_slots" type = "number" min = "0" class = "form-control">
                    </div>

                    <div class = "mb-3">
                        
                        <label class = "form-label">Status</label>

                        <select v-model = "form.status" class = "form-select">

                            <option value = "Open">Open</option>
                            <option value = "Closed">Closed</option>
                            <option value = "Cancelled">Cancelled</option>
                            <option value = "Completed">Started</option>
                            <option value = "Completed">On Going</option>
                            <option value = "Completed">Completed</option>

                        </select>
                    </div>

                    <button @click = "updateTrek()" class = "btn btn-primary">
                        Save Changes
                    </button>


                </div>

            </div>
        </div>

    </div>
</template>

<script>
import axios from "axios";

export default {
    name : "TrekStatusManagement",

    props : {
        trekId : [Number]
    },

    data() {
        return {
            trek : {},
            form : {
                available_slots : 0,
                status : "Open"
            }
        }
    },

    mounted() {
        this.fetchTrekDetails();
    },

    methods : {
        async fetchTrekDetails() {
            try {
                const token = localStorage.getItem("token");

                const res = await axios.get(`http://127.0.0.1:5000/api/staff/treks/${this.trekId}`, {
                    
                    headers : {

                        "Authorization" : `Bearer ${token}`

                    }
                });

                if (res.status === 200) {

                    this.trek = res.data;
                    this.form.available_slots = res.data.available_slots;
                    this.form.status = res.data.status;

                }
            } catch (error) {
                console.error("Error fetching trek details:", error);
                alert("Failed to load trek details.");
            }
        },

        async updateTrek() {

            try {
                const token = localStorage.getItem("token");

                await axios.post(`http://127.0.0.1:5000/api/staff/trek_update/${this.trekId}/slots`, this.form, {

                    headers : {

                        "Authorization" : `Bearer ${token}`
                    }
                });

                alert("Trek updated successfully.");
                this.goBack();
            } catch (error) {
                console.error("Error updating trek:", error);
                alert("Failed to update trek.");
            }
        },

        goBack() {
            this.$emit("go-back");
        }
    }
}
</script>
