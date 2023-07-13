export default [{
    method: 'POST',
    resource: '/auth',
    description: 'Get a session cookie',
    request: {
        username: 'admin',
        password: 'admin'
    },
    response: {
        success: true
    }
}, {
    resource: '/card',
    description: 'Get last unknown card',
    response: {
        id: 1,
        time: '2023-07-09T18:32:19.961Z',
        channel: 'INFO',
        message: 'Access denied for Card: 23456 Facility: 789'
    }
}, {
    method: 'POST',
    resource: '/database',
    description: 'Upload database via a file form field named file',
    request: 'multipart/form-data',
    response: {
        success: 'Restored from {filename}'
    }
}, {
    resource: '/database',
    description: 'Download database file backup',
    responseType: 'application/vnd.sqlite3'
}, {
    resource: '/events',
    description: null,
    request: '/api/events?channel=DEBUG&channel=INFO&limit=10&offset=0',
    response: [
        {
            id: 1,
            time: '2021-03-06T18:32:19.961Z',
            channel: 'DEBUG',
            message: 'User 2 created'
        }
    ]
}, {
    method: 'POST',
    resource: '/users',
    description: 'Create a user. Only name is required.',
    request: {
        name: 'First Last',
        pin: '0000',
        card: 23456,
        facility: 789
    },
    response: {
        id: 1,
        name: 'First Last',
        pin: '0000',
        card: 23456,
        facility: 789
    }
}, {
    resource: '/users',
    description: 'Get list of users',
    response: [
        {
            id: 42,
            name: 'First Last',
            pin: '0000',
            card: 23456,
            facility: 789
        }
    ]
}, {
    resource: '/users/{id}',
    description: 'Get a user by id',
    response: {
        id: 1,
        name: 'First Last',
        pin: '0000',
        card: 23456,
        facility: 789
    }
}, {
    method: 'PUT',
    resource: '/users/{id}',
    description: 'Update a user by id. Provide at least one property.',
    request: {
        name: 'First Last',
        pin: '0000',
        card: 23456,
        facility: 789
    },
    response: {
        id: 1,
        name: 'First Last',
        pin: '0000',
        card: 23456,
        facility: 789
    }
}, {
    method: 'DELETE',
    resource: '/users/{id}',
    description: 'Delete a user by id',
    responseCode: 204
}/* , {
    method: 'POST',
    resource: '/update',
    description: 'not implemented'
}, {
    resource: '/update',
    description: 'not implemented'
}, {
    method: 'POST',
    resource: '/reboot',
    description: 'not implemented'
} */];
