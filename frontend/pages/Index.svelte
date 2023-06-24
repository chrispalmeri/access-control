<script>
    import EventList from '../components/EventList.svelte';
    import UserList from '../components/UserList.svelte';
    import DatabaseCard from '../components/DatabaseCard.svelte';

    // how can you preserve events and users across spa navigation?
    // would be better if page does not reflow everytime
    // add a store probably
</script>

<!--
<div class="card">
    <h2>Index page</h2>

    <a href="#/login">Login</a>
    <a href="#/na">404 Page</a>
    <a href="/api">API</a>
</div>
-->

<EventList />

<UserList />

<DatabaseCard />
