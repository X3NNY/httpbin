import req from './api';
import Axios from 'axios'

export const postRegister = (password) => {
    return req.post('/register/', {password: password});
}

export const postLogin = (password) => {
    return req.post('/login/', {password: password});
}

export const postReapply = () => {
    return req.post('/reapply/');
}

export const getInfo = () => {
    return req.get('/info/');
}

export const getInfoRoutes = () => {
    return req.get('/info/routes/');
}

export const postAddRoute = (form) => {
    return req.post('/route/add/', form);
}

export const getRouteInfo = (id) => {
    return req.get(`/route/${id}/`);
}

export const postStatusChange = () => {
    return req.post('/change/');
}

export const postUpdateRouteInfo = (id, form) => {
    return req.post(`/route/${id}/`, form);
}

export const deleteRoute = (id) => {
    return req.delete(`/route/${id}/`);
}
export const getHttpLogDetail = (id) => {
    return req.get(`/info/${id}/detail/`);
}

export const getHttpLogByPage = (page, size, filters) => {
    return req.post(`/list/${page}/${size}/`, filters);
}

export const postSearchCT = (ct) => {
    return req.post('/search/ct/', {ct: ct});
}

export const postSearchIP = (ip) => {
    return req.post('/search/ip/', {ip: ip});
}

export const postDownload = (ids) => {
    return Axios({
        method: 'post',
        withCredentials: true,
        url: '/download/',
        data: {ids: ids},
        responseType: 'blob'
    })
}

export const postDownloadAll = () => {
    return Axios({
        method: 'post',
        withCredentials: true,
        url: '/download/all/',
        data: {},
        responseType: 'blob'
    })
}

export const postDelete = (ids) => {
    return req.post('/delete/', {ids: ids});
}

export const postDeleteAll = () => {
    return req.post('/delete/all/');
}

export const postDownloadFile = (hash) => {
    return Axios({
        method: 'post',
        withCredentials: true,
        url: `/file/${hash}/download/`,
        data: {},
        responseType: 'blob'
    })
}