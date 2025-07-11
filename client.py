import asyncio
import requests
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
import json

# Create PeerConnection
pc = RTCPeerConnection()

async def setup_audio():
    player = MediaPlayer("default", format="pulse", options={"channels": "1"})
    pc.addTrack(player.audio)

async def create_and_send_offer(signaling_server_url, my_id, peer_id):
    await setup_audio()
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    offer_data = {
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    }

    requests.post(f"{signaling_server_url}/send_offer", json={
        "to": peer_id,
        "offer": offer_data
    })

    await wait_for_answer(signaling_server_url, my_id)

async def wait_for_answer(signaling_server_url, my_id):
    while True:
        response = requests.get(f"{signaling_server_url}/get_offer/{my_id}")
        answer = response.json().get("answer")
        if answer:
            answer_desc = RTCSessionDescription(sdp=answer["sdp"], type=answer["type"])
            await pc.setRemoteDescription(answer_desc)
            print("Answer received and set!")
            break
        await asyncio.sleep(1)  # Poll every second

# Replace with actual IDs and server
signaling_server_url = "http://yourserver.com"
asyncio.run(create_and_send_offer(signaling_server_url, "caller_001", "callee_001"))
