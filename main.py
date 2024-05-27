from server.VMServer import VMServer
import asyncio

async def main():
    user = VMServer()
    while True:
        command = input().split(" ")

        match command[0]:
            case "connect":
                await user.connect(command[1], command[2], int(command[3]))
            
            case "disconnect":
                await user.disconnect()

            case "create":
                command = list(map(int, command[1:]))
                vinchester = command[2:]
                await user.create_vm(ram=command[0], cpu_cores=command[1], vinchester=vinchester)

            case "ls":
                await user.list_vm_all()
            case "lsc":
                await user.list_vm_connected()
            case "lsa":
                await user.list_vm_authored()
            case "exit":
                break

                



if __name__ == '__main__':
    asyncio.run(main())