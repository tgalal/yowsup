from Yowsup.connectionmanager import YowsupConnectionManager

def main():
    y = YowsupConnectionManager()

    signalsInterface = y.getSignalsInterface()
    methodsInterface = y.getMethodsInterface()

    signalsInterface.registerListener("auth_success", onAuthSuccess)
    methodsInterface.call("auth_login", ("918790911445", "620231"))

def onAuthSuccess(username):
    print("Logged in as {0}".format(username))

if __name__ == "__main__":
    main()
