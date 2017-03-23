<template>

<div class="row">
    <div class="col">
        <ul class="list-group">
            <li class="list-group-item" v-for="m in machines">
                {{m.username}}
            </li>
        </ul>
    </div>

</div>

</template>

<script>
    export default {
        data() {
            fetch("http://127.0.0.1:8888/u/machine_list")
                .then(function(response) {
                    reponse.json().then(function(json) {
                        return {
                            machine: json
                        }
                    })
                });
        }
    }
</script>