# Pagination

```html
{% if is_paginated %}
<nav aria-label="Page navigation">
    <ul class="pagination">
        {% if page_obj.has_previous %}
        <li class="page-item">
            <a
                class="page-link"
                href="{{ request.path }}?page={{ page_obj.previous_page_number }}"
                >
                Previous
            </a>
        </li>
        {% endif %}
        {% if page_obj.has_next %}
        <li class="page-item">
            <a
                class="page-link"
                href="{{ request.path }}?page={{ page_obj.next_page_number }}"
                >
                Next
            </a>
        </li>
        {% endif %}
    </ul>
</nav>
<p>
    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
</p>
{% endif %}
```
