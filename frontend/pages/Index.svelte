<script>
    import EventList from '../components/EventList.svelte';
    import UserList from '../components/UserList.svelte';
    import DatabaseCard from '../components/DatabaseCard.svelte';
</script>

<div class="card">
    <h2>Menu</h2>
    <p><a href="#/login">Login</a></p>
    <p><a href="#/na">404 Page</a></p>
    <p><a href="/api">API</a></p>
</div>

<EventList />

<UserList />

<DatabaseCard />
