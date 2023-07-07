import { writable } from 'svelte/store';

export const users = writable([]);

users.refresh = async function () {
    const response = await fetch('/api/users');
    if (response.status === 403) {
        users.set([]);
        location.replace('/login');
        return;
    }
    const data = await response.json();
    users.set(data);
};

export const events = writable([]);
