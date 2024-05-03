<script lang="ts">
    import type {Message} from './lib/types';
    export let message: Message;
</script>

<div class="message-row">
    <div class="message-bubble {message.sender}">
        <p>{message.message}</p>
    </div>
</div>

<style>
    .message-row {
        width: 100%;
        display: flex;
    }
    .message-bubble {
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        display: inline-block;
        width: auto;
        max-width: 60%;
    }
    .message-bubble p {
        margin: 0;
        color: white;
    }

    .you {
        background-color: #007bff;
        margin-left: auto;
    }

    .them {
        background-color: #28a745;
        margin-right: auto;
    }
</style>