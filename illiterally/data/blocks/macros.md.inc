{% macro ref(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {%- if __blk.is_rendered -%}
            [{{__blk.name}}]({{__blk.ref(__file__)}}#{{__blk.slug}})
        {%- else -%}
            <font color="red">RefMissingBlock({{__blk.slug}})</font>
        {%- endif -%}
    {%- else -%}
        <font color="red">RefInvalidSlug({{slug}})</font>
    {%- endif -%}
{% endmacro %}

{% macro ref_or_name(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {%- if __blk.is_rendered -%}
            [{{__blk.name}}]({{__blk.ref(__file__)}}#{{__blk.slug}})
        {%- else -%}
            {{ __blk.name }}
        {%- endif -%}
    {%- else -%}
        <font color="red">RefInvalidSlug({{slug}})</font>
    {%- endif -%}
{% endmacro %}

{% macro render(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {{ render_block(slug) }}
    {%- else -%}
        <font color="red">RenderInvalidSlug({{slug}})</font>
    {%- endif -%}
{% endmacro %}