<script lang="ts">
  import {onMount} from 'svelte';
  import type {Message} from './lib/types';
  import MessageBubble from './MessageBubble.svelte';

  let socket: WebSocket;
  let message_str: string;
  let messages: Message[] = [
  ];

  onMount(() => {
    socket = new WebSocket('ws://localhost:8000/chat');
    
    socket.onopen = () => {
      console.log('Connected to server');
    }

    socket.onmessage = (event) => {
      let message: Message = {
        sender: 'them',
        message: event.data
      };

      messages = [...messages, message];
    }
  })

  function sendMessage(event: Event) {
    if (!message_str) return;
    
    if (
      (event instanceof KeyboardEvent && event.key === 'Enter') || 
    (event instanceof MouseEvent && event.type === 'click')) {
    socket.send(message_str);
    
    let message: Message = {
      sender: 'you',
      message: message_str
    };

    messages = [...messages, message];

    message_str = '';

  }
    
  }

</script>

<div class="flex-container">
  <aside class="side"></aside>
  <main class="chat-window">
    <h1 class="title">Bravio</h1>
    <section class="messages">
      {#each messages as msg}
        <MessageBubble message={msg}/>
      {/each}
    </section>
    <section class="input">
      <input class="msg-box" type="text" placeholder="Type your message here" bind:value={message_str} on:keydown={sendMessage}/>
      <button class="send" on:click={sendMessage}>Send</button>
    </section>
  </main>
  <aside class="side"></aside>
</div>

<style>
  .flex-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  .side {
    flex: 2;
  }

  .chat-window {
    flex: 3;
    display: flex;
    flex-direction: column;
    height: 100%;
    align-items: center;
    justify-content: space-between;
    background-color: rgba(172, 255, 47, 0.172);
  }
  .title {
    font-size: 2rem;
    font-weight: 700;
    color: #333;
    margin: 1rem 0 2rem 0;
    text-align: center;
  }

  .input {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 1rem;
  }

  .msg-box {
    flex: 1;
    padding: 0.5rem;
    margin-right: 1rem;
    border: 1px solid #333;
    border-radius: 5px;
  }

  .send {
    padding: 0.5rem 1rem;
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .messages {
    width: 100%;
    height: 100%;
    padding: 1rem;
    overflow-y: scroll;
  }
</style>