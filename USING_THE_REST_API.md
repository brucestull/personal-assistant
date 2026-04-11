# Using the Item Location REST API

This runbook documents how to interact with the **Item Location** REST API,
which is provided by Django REST Framework (DRF).

---

## Authentication

The API uses **Session Authentication** and **Basic Authentication** (configured
globally in `settings.py`).

| Method | When to use |
|---|---|
| **Session Auth** | Browser / same-origin requests (login via `/accounts/login/`) |
| **Basic Auth** | `curl`, scripts, or any HTTP client |

All endpoints require the user to be authenticated **and** to have
`registration_accepted = True`.

---

## Base URL

```
/item-location/api/
```

The browsable DRF API is available at that URL when you are logged in through a
browser.

---

## Endpoints

### Storage Locations

| Method | URL | Description |
|---|---|---|
| GET | `/item-location/api/locations/` | List all your storage locations |
| POST | `/item-location/api/locations/` | Create a new storage location |
| GET | `/item-location/api/locations/{id}/` | Retrieve a specific location |
| PUT | `/item-location/api/locations/{id}/` | Fully update a location |
| PATCH | `/item-location/api/locations/{id}/` | Partially update a location |
| DELETE | `/item-location/api/locations/{id}/` | Delete a location |

### Items

| Method | URL | Description |
|---|---|---|
| GET | `/item-location/api/items/` | List all your items |
| POST | `/item-location/api/items/` | Create a new item |
| GET | `/item-location/api/items/{id}/` | Retrieve a specific item |
| PUT | `/item-location/api/items/{id}/` | Fully update an item |
| PATCH | `/item-location/api/items/{id}/` | Partially update an item |
| DELETE | `/item-location/api/items/{id}/` | Delete an item |

---

## Field Reference

### StorageLocation

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer | read-only | Auto-generated primary key |
| `name` | string (max 255) | **yes** | Human-readable name |
| `type` | string | **yes** | One of the choices below |
| `item_count` | integer | read-only | Number of items stored here |
| `created` | datetime | read-only | ISO 8601 |
| `updated` | datetime | read-only | ISO 8601 |

**`type` choices:** `room`, `cabinet`, `shelf`, `drawer`, `box`, `bin`,
`closet`, `garage`, `attic`, `basement`, `other`

### Item

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer | read-only | Auto-generated primary key |
| `name` | string (max 255) | **yes** | Human-readable name |
| `type` | string | **yes** | One of the choices below |
| `location` | integer or null | no | PK of a StorageLocation owned by you |
| `location_name` | string or null | read-only | Display name of the location |
| `created` | datetime | read-only | ISO 8601 |
| `updated` | datetime | read-only | ISO 8601 |

**`type` choices:** `tool`, `clothing`, `electronics`, `document`, `food`,
`book`, `toy`, `sports`, `kitchen`, `furniture`, `other`

---

## Examples with `curl`

Replace `<username>` and `<password>` with your credentials.
Replace `<host>` with your server address (e.g. `http://localhost:8000`).

### List storage locations

```bash
curl -u <username>:<password> \
     <host>/item-location/api/locations/
```

### Create a storage location

```bash
curl -u <username>:<password> \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"name": "Garage Shelf", "type": "shelf"}' \
     <host>/item-location/api/locations/
```

### Retrieve a storage location

```bash
curl -u <username>:<password> \
     <host>/item-location/api/locations/1/
```

### Update a storage location (full)

```bash
curl -u <username>:<password> \
     -X PUT \
     -H "Content-Type: application/json" \
     -d '{"name": "Garage Top Shelf", "type": "shelf"}' \
     <host>/item-location/api/locations/1/
```

### Partially update a storage location

```bash
curl -u <username>:<password> \
     -X PATCH \
     -H "Content-Type: application/json" \
     -d '{"name": "Garage Bottom Shelf"}' \
     <host>/item-location/api/locations/1/
```

### Delete a storage location

```bash
curl -u <username>:<password> \
     -X DELETE \
     <host>/item-location/api/locations/1/
```

---

### List items

```bash
curl -u <username>:<password> \
     <host>/item-location/api/items/
```

### Create an item (with a location)

```bash
curl -u <username>:<password> \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"name": "Cordless Drill", "type": "tool", "location": 1}' \
     <host>/item-location/api/items/
```

### Create an item (no location)

```bash
curl -u <username>:<password> \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"name": "Spare Key", "type": "other"}' \
     <host>/item-location/api/items/
```

### Update an item's location

```bash
curl -u <username>:<password> \
     -X PATCH \
     -H "Content-Type: application/json" \
     -d '{"location": 2}' \
     <host>/item-location/api/items/3/
```

### Remove an item's location (set to unassigned)

```bash
curl -u <username>:<password> \
     -X PATCH \
     -H "Content-Type: application/json" \
     -d '{"location": null}' \
     <host>/item-location/api/items/3/
```

### Delete an item

```bash
curl -u <username>:<password> \
     -X DELETE \
     <host>/item-location/api/items/3/
```

---

## Browsable API (Browser)

1. Log in at `<host>/accounts/login/`.
2. Navigate to `<host>/item-location/api/` in your browser.
3. DRF's HTML interface lets you browse, create, update, and delete records
   interactively without needing `curl`.

---

## Using the Vue.js Single-Page App

A built-in Vue.js app is also available at `/item-location/spa/`. It communicates
with the REST API endpoints above using your browser session cookie.  No
additional authentication setup is needed when accessing the SPA through a browser.

---

## Error Responses

| Status | Meaning |
|---|---|
| 400 | Validation error – check the JSON body for field errors |
| 401 | Not authenticated |
| 403 | Authenticated but not authorised (e.g. `registration_accepted = False`) |
| 404 | Object not found or belongs to another user |
| 405 | HTTP method not allowed |
