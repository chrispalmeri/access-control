<script>
import UserCreate from './UserCreate.svelte';
import UserUpdate from './UserUpdate.svelte';
import UserDelete from './UserDelete.svelte';

async function get() {
    const response = await fetch('/api/users');
    const data = await response.json();

    if (response.ok && data.length > 0) {
        return data;
    } else {
        throw new Error('No items to show');
    }
}

let api = get();

// option
//var pin = user.pin ? user.pin.replace(/./g, '*') : '';
//var card = user.card && user.facility ? user.card.replace(/./g, '*') : '';

</script>

<div class="card">
    <h2>Users</h2>
    <UserCreate />
    {#await api then users}
    <table>
        <tr>
            <th>Name</th>
            <th>Pin</th>
            <th>Card</th>
            <th></th>
        </tr>
        {#each users as user}
        <tr>
            <td>{user.name}</td>
            <td>{user.pin || ''}</td>
            <td>{user.card || ''}</td>
            <td><UserUpdate user={user} /> <UserDelete id={user.id} /></td>
        </tr>
        {/each}
    </table>
    {:catch error}
    <p>{error.message}</p>
    {/await}
</div>
