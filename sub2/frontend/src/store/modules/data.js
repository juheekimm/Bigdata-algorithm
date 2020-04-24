import api from "../../api";

// initial state
const state = {
    storeSearchList: [],
    storeSearchPage: "0",
    store: {
        id: "",
        name: "",
        branch: "",
        area: "",
        tel: "",
        address: "",
        lat: 0.0,
        lng: 0.0,
        categories: []
    },
    token: "",
    user: {},
    count: 0,
};

// actions
const actions = {
    async getStores({ commit }, params) {
        const append = params.append;
        const resp = await api.getStores(params);
        const stores = resp.data.results.map(d => ({
            id: d.id,
            name: d.store_name,
            branch: d.branch,
            area: d.area,
            tel: d.tel,
            address: d.address,
            lat: d.latitude,
            lng: d.longitude,
            categories: d.category_list
        }));

        if (append) {
            commit("addStoreSearchList", stores);
        } else {
            commit("setStoreSearchList", stores);
        }
        commit("setStoreSearchPage", resp.data.next);
    }
};

// mutations
const mutations = {
    setStoreSearchList(state, stores) {
        state.storeSearchList = stores.map(s => s);
    },
    addStoreSearchList(state, stores) {
        state.storeSearchList = state.storeSearchList.concat(stores);
    },
    setStoreSearchPage(state, payload) {
        state.storeSearchPage = payload
    },
    incrementStoreSearchPage(state) {
        state.storeSearchPage++
    },
    setToken(state, payload) {
        state.token = payload
    },
    setUser(state, payload) {
        state.user = payload
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations
};