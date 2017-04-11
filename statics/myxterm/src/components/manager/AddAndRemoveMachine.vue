<template>


    <div class="col-auto">
        <div v-if="res_success" class="alert alert-success alert-dismissible fade show" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            {{res_state}}
        </div>
        <div v-if="res_fail" class="alert alert-danger alert-dismissible fade show" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            {{res_state}}
        </div>
        <div class="input-group ma">
            <span class="input-group-addon" id="basic-addon1">Username</span>
            <input type="text" class="form-control" placeholder="Username" aria-describedby="basic-addon1" name="username" v-model="username">
        </div>
        <div class="input-group ma">
            <span class="input-group-addon" id="basic-addon1">password</span>
            <input type="password" class="form-control" placeholder="password" aria-describedby="basic-addon1" username="password" v-model="password">
        </div>
        <button type="button" class="btn btn-warning ma" v-on:click="submit">ADD</button>
    </div>



</template>

<script>
import BaseURL from '../../config.js'

    export default{
        data: {
            username: '',
            password: '',
            res_success: false,
            res_fail: false,
            res_state: '',
        },
        methods: {
            submit: function(event){
                if(this.username === '' | this.password === ''){
                    return
                } 
                console.log(this.username)
                fetch(BaseURL + '/u/add_machine', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },     
                    body: 'username=' + this.username + '&' + 'password=' + this.password,
                })
                .then((response) => {
                    return response.json()
                })
                .then((data) => {
                    res_state = data.message;
                    if(data.ok){
                        this.res_success = true;
                    }else{
                        this.res_fail = true;
                    }
                });
            }
        }
    }
</script>

<style>
.ma{
    margin-top: 1rem;
}
</style>
