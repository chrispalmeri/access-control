import { writable } from 'svelte/store';

export const users = writable([]);

users.refresh = async function () {
    const response = await fetch('/api/users');
    const data = await response.json();
    users.set(data);
};
