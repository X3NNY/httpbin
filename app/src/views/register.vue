<template>
    <div style="margin: 30vh auto;width: 30vw" @keyup.enter="handleRegisterClick">
        <el-card style="width: 30vw;" shadow="hover">
            <template #header>
                <div class="card-header">
                    Register
                    <router-link to="/login">
                        <el-button type="primary" text size="small">Login</el-button>
                    </router-link>
                </div>
            </template>
            <el-input style="margin: 5vh auto;" placeholder="password" v-model="password"></el-input>
        </el-card>
    </div>
</template>

<script>
import { reactive, toRefs } from 'vue-demi'
import { postRegister } from '../api/httpbin';
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router';
export default {
    setup() {
        const state = reactive({
            password: ''
        });

        const router = useRouter();

        const handleRegisterClick = () => {
            postRegister(state.password).then(res => {
                if (res.code === 200) {
                    ElMessage({
                        message: 'Congrats, register success.',
                        type: 'success',
                    });
                    router.push('/login');
                } else if (res.code === 201) {
                    ElMessage({
                        message: 'Password invaild.',
                        type: 'danger',
                    })
                } else if (res.code === 202) {
                    ElMessage({
                        message: 'Password exists.',
                        type: 'warning',
                    })
                }
            })
        }

        return {
            ...toRefs(state),
            handleRegisterClick
        }
    }
}
</script>