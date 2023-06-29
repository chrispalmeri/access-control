import Router from 'svelte-spa-router';
import './css/global.css';
import Index from './pages/Index.svelte';
import Login from './pages/Login.svelte';
import NotFound from './pages/NotFound.svelte';

const routes = {
    // Exact path
    '/': Index,
    '/login': Login,

    // Using named parameters, with last being optional
    // '/author/:first/:last?': Author,

    // Wildcard parameter
    // '/book/*': Book,

    // Catch-all
    // This is optional, but if present it must be the last
    '*': NotFound
};

const app = new Router({
    target: document.body,
    props: {
        routes: routes
    }
});

export default app;
