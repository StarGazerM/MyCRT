import Vue from 'vue'
import VueRouter from 'vue-router'

// root
import CRTManager from './components/CRTManager.vue'
import CurrentCRT from './components/CurrentCRT.vue'

// crt-manager
import AddAndRemoveMachine from './components/manager/AddAndRemoveMachine.vue'
import MachineList from './components/manager/MachineList.vue'
import ChangePassword from './components/manager/ChangePassword.vue'

Vue.use(VueRouter)

// current-crt
const CRT = {}

const routes = [{
        path: '/current-crt',
        component: CurrentCRT,
        // children: [{
        //     path: ':id',
        //     component: CRT,
        // }]
    },
    {
        path: '/crt-manager',
        component: CRTManager,
        children: [{
                path: 'machine-list',
                component: MachineList,
            },
            {
                path: 'add-remove',
                component: AddAndRemoveMachine,
            },
            {
                path: 'password',
                component: ChangePassword
            },
        ]
    }
]

const router = new VueRouter({
    routes
})

const dashboard = new Vue({
    router
}).$mount('#dashboard')