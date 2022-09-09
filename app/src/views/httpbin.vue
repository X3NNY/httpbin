<template>
<div>
    <el-row :gutter="10" style="margin: .5vw 1vh;">
        <el-col :span="18">
            <el-card>
                <el-space>
                    <el-input placeholder="search Path" v-model="filters.path" style="width: 16vw" @keyup.enter="toPage(1)">
                        <template #suffix>
                            <el-icon class="el-input__icon input-suffix-icon" @click="toPage(1)" style="cursor: pointer"><Search /></el-icon>
                        </template>
                    </el-input>
                    <el-button @click="handleDownloadClick">
                        Download <el-icon class="el-icon--right"><Download /></el-icon>
                    </el-button>
                    <el-button type="primary" @click="toPage(1)">
                        Reload <el-icon class="el-icon--right"><RefreshRight /></el-icon>
                    </el-button>
                    <el-button type="danger" @click="handleDeleteClick">
                        Delete <el-icon class="el-icon--right"><Delete /></el-icon>
                    </el-button>
                </el-space>
                <el-button @click="handleSpreadClick" style="float: right"><el-icon><ArrowLeft v-if="!isSpread"/><ArrowDown v-else/></el-icon></el-button>
                <el-form v-if="isSpread" label-width="140px" style="margin-top: 1.5vh;">
                    <el-form-item label="Method: ">
                        <el-select v-model="filters.method">
                            <el-option label="ALL" :value="0"></el-option>
                            <el-option label="GET" :value="1"></el-option>
                            <el-option label="POST" :value="2"></el-option>
                            <el-option label="OPTIONS" :value="3"></el-option>
                            <el-option label="HEAD" :value="4"></el-option>
                            <el-option label="PUT" :value="5"></el-option>
                            <el-option label="DELETE" :value="6"></el-option>
                            <el-option label="PATCH" :value="7"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Content-Type: ">
                        <el-autocomplete :fetch-suggestions="queryCT" :trigger-on-focus="false" placeholder="search Content-Type address" v-model="filters.ct" style="width: 16vw"></el-autocomplete>
                    </el-form-item>
                    <el-form-item label="IP: ">
                        <el-autocomplete :fetch-suggestions="queryIP" :trigger-on-focus="false" placeholder="search IP address" v-model="filters.ip" style="width: 16vw"></el-autocomplete>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="toPage(1)">Search<el-icon class="el-icon--right"><Search /></el-icon></el-button>
                    </el-form-item>
                </el-form>
                <el-table :data="httplogs" @row-click="handleHttplogDetailClick" :row-style="{'cursor': 'pointer'}" style="margin: 0 1vh;min-height: 20vh" stripe>
                    <el-table-column prop="id" label="ID" width="70"></el-table-column>
                    <el-table-column prop="path" label="Path">
                        <template #default="scope">
                            <span>{{ scope.row.path }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="ip" label="IP" width="130"></el-table-column>
                    <el-table-column prop="method" label="Method" width="75">
                        <template #default="scope">
                            {{ ['', 'GET', 'POST', 'OPTIONS', 'HEAD', 'PUT', 'DELETE', 'PATCH'][scope.row.method] }}
                        </template>
                    </el-table-column>
                    <el-table-column prop="ua" label="User-Agent" width="130">
                        <template #default="scope">
                            {{ scope.row.ua.indexOf(' ') != -1 ? scope.row.ua.substr(0, scope.row.ua.indexOf(' ')) : scope.row.ua}}
                        </template>
                    </el-table-column>
                    <el-table-column prop="ct" label="Content-Type" width="235">
                        <template #default="scope">
                            {{ scope.row.ct.indexOf(';') != -1 ? scope.row.ct.substr(0, scope.row.ct.indexOf(';')) : scope.row.ct}}
                        </template>
                    </el-table-column>
                    <el-table-column label="Date(UTC+0)" width="155">
                        <template #default="scope">
                            {{ new Date(scope.row.date*1000).format('yy/MM/dd hh:mm:ss') }}
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination
                    small
                    background
                    hide-on-single-page
                    layout="prev, pager, next"
                    :total="total"
                    :page-size="pageSize"
                    style="float: right;margin: .5vw 0;"
                    @current-change="toPage"
                ></el-pagination>
            </el-card>
        </el-col>
        <el-col :span="6">
            <el-space style="margin: 1vh 0;">
                <el-button type="primary" size="small" @click="handleDownloadAllClick">Download ALL<el-icon class="el-icon--right"><Download /></el-icon></el-button>
                <el-button type="danger" size="small" @click="handleDeleteAllClick">Delete ALL<el-icon class="el-icon--right"><Delete /></el-icon></el-button>
                <el-button type="success" size="small" @click="handleReapplyClick">Re-apply<el-icon class="el-icon--right"><Refresh /></el-icon></el-button>
            </el-space>
            <el-card>
                <div class="my-label">
                    <b>Identifier: </b>
                    <el-input v-model="identifier" style="width: 15vw">
                        <template #suffix>
                            <el-icon class="el-input__icon input-suffix-icon" @click="writeClipBoard(identifier)"><DocumentCopy /></el-icon>
                        </template>
                    </el-input>
                </div>
                <div class="my-label">
                    <b>Status: </b>
                    <b @click="handleStatusChange" style="cursor: pointer;"> 
                        <div v-if="status"><div class="success-circle" />Running</div>
                        <div v-else><div class="danger-circle" />Stop</div>
                    </b>
                </div>
                <div class="my-label">
                    <b>Total: </b>
                    <b>
                        {{ total_count }}
                    </b>
                </div>
                <div class="my-label">
                    <b>Routes: </b>
                    <b>{{ route_count }}</b>
                </div>
            </el-card>
            <el-card style="margin-top: 1vh" class="custom-route">
                <template #header>
                    <div class="card-header">
                    Custom Route
                    <el-button @click="handleAddRouteClick">New <el-icon><EditPen /></el-icon></el-button>
                    </div>
                </template>
                <el-table :data="routes" stripe border :show-header="false">
                    <el-table-column prop="path"></el-table-column>
                    <el-table-column width="80">
                        <template #default="scope">
                            <el-space>
                                <el-button type="primary" size="small" style="padding: 2px 5px;" @click="handleLoadRoute(scope.row.id)">
                                    <el-icon><Edit /></el-icon>
                                </el-button>
                                <el-button type="danger" size="small" style="padding: 2px 5px;" @click="handleDeleteRoute(scope.row.id)">
                                    <el-icon><Delete /></el-icon>
                                </el-button>
                            </el-space>
                        </template>
                    </el-table-column>
                </el-table>
            </el-card>
        </el-col>
    </el-row>
    <el-row :gutter="10" style="margin: .5vw 1vh;">
        <el-col>
            <el-card v-if="isDetailCardDisplay" v-loading="isDetailCardLoading" element-loading-text="Loading...">
                <div class="my-label-up">
                    <div style="width: 50vw">
                        <el-form-item label="ID: ">
                            <el-space>{{ detail.row.id }}<el-button @click="handleDownloadRaw(detail.row.id)">Download Raw <el-icon class="el-icon--right"><Download /></el-icon></el-button></el-space>
                        </el-form-item>
                        <v-md-preview :text="detail.raw">
                        </v-md-preview>
                    </div>
                    <el-form style="width: 40vw;margin-top: 4vh" label-width="120px">
                        <el-form-item label="IP: ">
                            {{ detail.row.ip }} <el-icon @click="writeClipBoard(detail.row.ip)"><DocumentCopy /></el-icon>
                        </el-form-item>
                        <el-form-item label="User-Agent: ">
                            {{ detail.row.ua }} <el-icon @click="writeClipBoard(detail.row.ua)"><DocumentCopy /></el-icon>
                        </el-form-item>
                        <el-form-item label="Content-Type: ">
                            {{ detail.row.ct }} <el-icon @click="writeClipBoard(detail.row.ct)"><DocumentCopy /></el-icon>
                        </el-form-item>
                        <el-form-item label="GET: ">
                            <ul style="list-style: none">
                                <li v-for="value,key of detail.get" :key="key">
                                    <el-button>{{key}}</el-button> = <el-button @click="writeClipBoard(value)">{{value}}</el-button>
                                </li>
                            </ul>
                        </el-form-item>
                        <el-form-item label="POST: ">
                            <ul style="list-style: none">
                                <li v-for="value,key in detail.post" :key="key">
                                    <el-button>{{key}}</el-button> =
                                    <span v-if="typeof(value) == 'String' "><el-button @click="writeClipBoard(value)">{{value}}</el-button></span>
                                    <span v-else>
                                        <el-button v-for="v of value" :key="v[0]" @click="handleDonwloadFile(v[0], v[1])">{{`${v[1]} (${(v[2] / 1024).toFixed(2)}KB)`}}</el-button>
                                    </span>
                                </li>
                            </ul>
                        </el-form-item>
                    </el-form>
                </div>
            </el-card>
        </el-col>
    </el-row>
    <el-dialog v-model="isAddRouteDialogDisplay" width="60%">
        <el-form label-width="80px">
            <el-form-item label="Path: ">
                <el-input v-model="route.path" placeholder="path..."></el-input>
            </el-form-item>
            <el-form-item label="Response: ">
                <el-upload with-credentials :ref="upload" :http-request="handleAddRoute" :limit="1" :on-exceed="handleExceed" :auto-upload="false">
                    <template #trigger>
                        <el-button>Response File <el-icon class="el-icon--right"><Document /></el-icon></el-button>
                    </template>
                    <template #tip>
                        <div style="color:brown;font-size: small;">
                            upload file will cover text input
                        </div>
                    </template>
                </el-upload>
                <el-input v-model="route.response" type="textarea" placeholder="Input response content..."></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="isAddRouteDialogDisplay = false">Close<el-icon class="el-icon--right"><Close /></el-icon></el-button>
            <el-button @click="handleAddRouteSubmit" type="primary">Submit<el-icon class="el-icon--right"><Check /></el-icon></el-button>
        </template>
    </el-dialog>
    </div>
</template>

<script>
import { onMounted, onUnmounted, reactive, ref, toRefs } from 'vue-demi';
import '@/utils/format';
import { getHttpLogByPage, getHttpLogDetail, getInfo, getInfoRoutes, postReapply, postSearchCT, postSearchIP, postDownload, postDownloadAll, postDelete, postDeleteAll, postDownloadFile, postAddRoute, getRouteInfo, deleteRoute, postUpdateRouteInfo, postStatusChange} from '../api/httpbin';
import { ElMessage } from 'element-plus';

export default {
    setup() {
        const state = reactive({
            httplogs: [],
            status: false,
            route_count: 0,
            date: 0,
            total_count: 0,

            identifier: '',
            page: 1,
            pageSize: 10,
            total: 0,

            routes: [],

            detail: {
                row: {},
                raw: '',
                get: {},
                post: {}
            },

            filters: {
                ip: '',
                path: '',
                method: 0,
                ct: ''
            },

            route: {
                path: '',
                response: '',
                file: '',
                id: undefined
            },

            interval: null,

            isSpread: false,
            isHttpLogLoading: false,
            isDetailCardDisplay: false,
            isDetailCardLoading: false,
            isAddRouteDialogDisplay: false,
            isEditRouteDialogDisplay: false,
        });

        const init = () => {
            getInfo().then(res => {
                if (res.code === 200) {
                    state.identifier = res.data.identifier;
                    state.status = res.data.status;
                    state.route_count = res.data.routes;
                    state.date = res.data.date;
                    state.total_count = res.data.total;
                }
            });
            getRoutes();
            toPage(1);
        }

        const getRoutes = () => {
            getInfoRoutes().then(res => {
                if (res.code === 200) {
                    state.routes = res.data;
                }
            })
        }

        const toPage = (page) => {
            state.page = page;
            state.isHttpLogLoading = true;
            getHttpLogByPage(state.page, state.pageSize, state.filters).then(res => {
                if (res.code === 200) {
                    state.httplogs = res.data.httplogs;
                    state.total = res.data.total;

                    if (state.total > state.total_count) {
                        state.total_count = state.total;
                    }
                    state.isHttpLogLoading = false;
                }
            })
        }

        const handleHttplogDetailClick = (row) => {
            state.isDetailCardDisplay = true;
            state.isDetailCardLoading = true;
            getHttpLogDetail(row.id).then(res => {
                if (res.code === 200) {
                    state.detail.row = row;
                    state.detail.raw = '```txt\n' + Buffer.from(res.data.raw, 'base64') + '\n```';
                    state.detail.get = res.data.get;
                    state.detail.post = res.data.post;
                    state.isDetailCardLoading = false;
                }
            })
        }

        const queryCT = (value, cb) => {
            postSearchCT(value).then(res => {
                let names = [];
                for (let name of res.data) {
                    names.push({value:name});
                }
                cb(names);
            })
        }

        const queryIP = (value, cb) => {
            postSearchIP(value).then(res => {
                let names = [];
                for (let name of res.data) {
                    names.push({value:name});
                }
                cb(names);
            })
        }
        
        const downloadFile = (res, fname) => {
            let data = res.data;
            let url = window.URL.createObjectURL(new Blob([data]))
            let a = document.createElement('a')
            a.style.display = 'none'
            a.href = url
            a.setAttribute('download', fname)
            document.body.appendChild(a)
            a.click()
            window.URL.revokeObjectURL(a.href)
            document.body.removeChild(a)
        }

        const handleDonwloadFile = (hash, filename) => {
            console.log(hash, filename, state.detail)
            ElMessage({
                message: 'Start download.',
                type: 'success',
            })
            postDownloadFile(hash).then(res => {
                downloadFile(res, filename);
            })
        }

        const handleDownloadClick = () => {
            let ids = state.httplogs.map(item => item.id);
            ElMessage({
                message: 'Start download.',
                type: 'success',
            })
            postDownload(ids).then(res => {
                downloadFile(res, "achieve.zip");
            })
        }

        const handleDownloadRaw = (id) => {
            ElMessage({
                message: 'Start download.',
                type: 'success',
            })
            postDownload([id]).then(res => {
                downloadFile(res, "achieve.zip");
            })
        }

        const handleDownloadAllClick = () => {
            ElMessage({
                message: 'Start download.',
                type: 'success',
            })
            postDownloadAll().then(res => {
                downloadFile(res, "achieve.zip");
            })
        }

        const handleDeleteClick = () => {
            let ids = state.httplogs.map(item => item.id);
            postDelete(ids).then(res => {
                ElMessage({
                    message: 'Delete done.',
                    type: 'success',
                });
                toPage(1);
            })
        }

        const handleDeleteAllClick = () => {
            postDeleteAll().then(res => {
                ElMessage({
                    message: 'Delete done.',
                    type: 'success',
                });
                toPage(1);
                state.isDetailCardDisplay = false;
            })
        }

        const handleReapplyClick = () => {
            postReapply().then(res => {
                init();
            })
        }

        const writeClipBoard = (content) => {
            let aux = document.createElement("input"); 
            aux.setAttribute("value", content); 
            document.body.appendChild(aux); 
            aux.select();
            document.execCommand("copy");
            document.body.removeChild(aux);
            ElMessage({
                message: 'Copied done.',
                type: 'success'
            })
            return true;
        }

        const handleSpreadClick = () => {
            if (state.isSpread) {
                state.isSpread = false;
            } else {
                state.isSpread = true;
            }
        }

        const handleAddRouteClick = () => {
            state.isAddRouteDialogDisplay = true;
        }

        const handleExceed = (files) => {
            upload.value.clearFiles();
            const file = files[0];
            upload.value.handleStart(file);
        }

        const handleAddRoute = (file) => {
            state.route.file = file;
            state.route.id = undefined;
        }

        const handleAddRouteSubmit = () => {
            if (state.route.id) {
                return handleEditRoute(state.route.id);
            }
            let formData = new FormData();
            formData.append('file', state.route.file);
            formData.append('path', state.route.path);
            formData.append('response', state.route.response);
            postAddRoute(formData).then(res => {
                if (res.code === 200) {
                    ElMessage({
                        message: 'Add Custom Route Success.',
                        type: 'success'
                    })
                    state.isAddRouteDialogDisplay = false;
                    getRoutes();
                } else if (res.code === 201) {
                    ElMessage({
                        message: 'Path must start with \'/\'.',
                        type: 'error'
                    })
                } else if (res.code === 202) {
                    ElMessage({
                        message: 'Path exists.',
                        type: 'error'
                    })
                }
            })
        }

        const handleLoadRoute = (id) => {
            state.route.id = id;
            getRouteInfo(id).then(res => {
                state.isAddRouteDialogDisplay = true;
                state.route.path = res.data.path;
                state.route.response = Buffer.from(res.data.response, 'Base64');
            })
        }

        const handleEditRoute = (id) => {
            let formData = new FormData();
            formData.append('file', state.route.file);
            formData.append('path', state.route.path);
            formData.append('response', state.route.response);
            postUpdateRouteInfo(id, formData).then(res => {
                if (res.code === 200) {
                    ElMessage({
                        message: 'Update Custom Route Success.',
                        type: 'success'
                    })
                    state.isAddRouteDialogDisplay = false;
                    getRoutes();
                } else if (res.code === 201) {
                    ElMessage({
                        message: 'Path must start with \'/\'.',
                        type: 'error'
                    })
                } else if (res.code === 202) {
                    ElMessage({
                        message: 'Path exists.',
                        type: 'error'
                    })
                }
            })
        }

        const handleDeleteRoute = (id) => {
            deleteRoute(id).then(res => {
                ElMessage({
                    message: "Delete done."
                })
            })
            getRoutes();
        }

        const handleStatusChange = () => {
            postStatusChange().then(res => {
                getInfo().then(res => {
                    if (res.code === 200) {
                        state.identifier = res.data.identifier;
                        state.status = res.data.status;
                        state.route_count = res.data.routes;
                        state.date = res.data.date;
                        state.total_count = res.data.total;
                    }
                });
            })
            
        }

        onUnmounted(() => {
            if (state.interval) {
                clearInterval(state.interval);
            }
        })

        onMounted(() => {
            state.interval = setInterval(() => {
                if (state.page == 1) {
                    toPage(state.page)
                }
            }, 3000)
        })

        const upload = ref();

        init();

        return {
            ...toRefs(state),
            handleSpreadClick,
            handleHttplogDetailClick,
            handleStatusChange,
            toPage,

            handleDownloadClick,
            handleDownloadAllClick,
            handleDeleteClick,
            handleDeleteAllClick,
            handleReapplyClick,
            handleDonwloadFile,

            queryCT,
            queryIP,

            writeClipBoard,
            handleAddRouteClick,
            handleExceed,
            handleAddRoute,
            handleAddRouteSubmit,
            handleLoadRoute,
            handleEditRoute,
            handleDeleteRoute,
            handleDownloadRaw,
        }
    }
}
</script>

<style lang="scss">
.vuepress-markdown-body:not(.custom) {
    padding: unset !important;
}
.vuepress-markdown-body div[class*="v-md-pre-wrapper-"] {
    border-radius: unset !important;
}
.input-suffix-icon {
    cursor: pointer;
    :hover {
        color: var(--el-border-color);
    }
}
.my-label {
    display: flex;
    align-items: center;
    margin: 0.5vh 0;
    justify-content: space-between;
}
.my-label-up {
    display: flex;
    margin: 0.5vh 0;
    justify-content: space-between;
}

.primary-circle {
    width: 10px;
    height: 10px;
    background-color: var(--el-color-primary);
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
}

.success-circle {
    width: 10px;
    height: 10px;
    background-color: var(--el-color-success);
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
}

.danger-circle {
    width: 10px;
    height: 10px;
    background-color: var(--el-color-danger);
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
}

.custom-route .el-card__body {
    padding: 0 0;
}
</style>