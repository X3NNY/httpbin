import Axios from 'axios';

const instance = Axios.create({
    baseURL: '/',
    timeout: 30000,
    withCredentials: true,
})

instance.interceptors.request.use((config) => {
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    return config
}, (err) => {
    console.log(err)
    return Promise.reject(err)
})

instance.interceptors.response.use((res) => {
    if (res.data.code === 403) {
        window.location.href = '#/login'
    }
    return res.data
}, (err) => {
    return Promise.reject(err)
})

export default {
    get: (path, data=null) => instance.get(path, {params: data}),
    post: (path, data=null) => instance.post(path, data),
    put: (path, data=null) => instance.put(path, data),
    delete: (path, data=null) => instance.delete(path, {params: data})
}