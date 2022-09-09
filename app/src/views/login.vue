<template>
    <div style="margin: 30vh auto;width: 30vw" @keyup.enter="handleLoginClick">
        <el-card style="width: 30vw;" shadow="hover">
            <template #header>
                <div class="card-header">
                    Login
                    <router-link to="/register">
                        <el-button type="primary" text size="small">Register</el-button>
                    </router-link>
                </div>
            </template>
            <el-input style="margin: 5vh auto;" placeholder="password" v-model="password"></el-input>
        </el-card>
    </div>
</template>

<script>
import { reactive, toRefs } from 'vue-demi'
import { postLogin } from '../api/httpbin';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus/lib/components';

export default {
    setup() {
        const state = reactive({
            password: ''
        });

        const router = useRouter();

        const handleLoginClick = () => {
            postLogin(state.password).then(res => {
                if (res.code === 200) {
                    localStorage.setItem('httpbin_login', res.data.toString());
                    router.push('/')
                } else {
                    ElMessage({
                        message: 'Password not exists or invaild.',
                        type: 'warning'
                    })
                }
            })
        }

        return {
            ...toRefs(state),
            handleLoginClick
        }
    }
}
</script>