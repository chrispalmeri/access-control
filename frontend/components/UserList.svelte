<script>
    import UserCreate from './UserCreate.svelte';
    import UserUpdate from './UserUpdate.svelte';
    import UserDelete from './UserDelete.svelte';
    import { users } from '../stores.js';

    users.refresh();

    // option
    //var pin = user.pin ? user.pin.replace(/./g, '*') : '';
    //var card = user.card && user.facility ? user.card.replace(/./g, '*') : '';
</script>

<div class="card">
    <h2>Users</h2>
    <p>
        <UserCreate />
    </p>
    {#if $users.length > 0}
    <table>
        <tr>
            <th>Name</th>
            <th>Pin</th>
            <th>Card</th>
            <th>Actions</th>
        </tr>
        {#each $users as user (user.id)}
        <tr>
            <td>{user.name}</td>
            <td>{user.pin || ''}</td>
            <td>{user.card || ''}</td>
            <td class="end smallgap"><UserUpdate user={user} /> <UserDelete user={user} /></td>
        </tr>
        {/each}
    </table>
    {:else}
    <p>No items to show</p>
    {/if}
</div>
