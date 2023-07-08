<script>
    import EventList from '../components/EventList.svelte';
    import UserList from '../components/UserList.svelte';
    import DatabaseCard from '../components/DatabaseCard.svelte';
    import ThemeSwitch from '../components/ThemeSwitch.svelte';
    import Footer from '../components/Footer.svelte';

    async function logout(event) {
        event.preventDefault();

        const response = await fetch('/api/auth', {
            method: 'DELETE'
        });

        if (response.ok) {
            location.replace('/login');
        }
    }
</script>

<ThemeSwitch />

<main>
    <div class="card">
        <h2>Menu</h2>
        <p><a href="/login">Login</a></p>
        <p><a href="/login" on:click={logout}>Logout</a></p>
        <p><a href="/na">404 Page</a></p>
        <p><a href="/api">API</a></p>
    </div>

    <EventList />

    <UserList />

    <DatabaseCard />
</main>

<Footer />
