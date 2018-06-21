
class BusinessNotificationProtocolEntity(NotificationProtocolEntity):
    """
    <notification type="business" offline="2" from="573114393962@s.whatsapp.net" id="540203522" t="1529166405">
        <profile jid="573114393962@s.whatsapp.net" tag="4228454263">
        <address>
        Calle 37 #28b-42
        HEX:43616c6c6520333720233238622d3432
        </address>
        <latitude>
        4.626062393188477
        HEX:342e363236303632333933313838343737
        </latitude>
        <longitude>
        -74.07843780517578
        HEX:2d37342e3037383433373830353137353738
        </longitude>
        <email>
        redes@petro.com.co
        HEX:726564657340706574726f2e636f6d2e636f
        </email>
        <description>
        Perfil oficial del dirigente político progresista Colombiano Gustavo Petro. Por una #ColombiaHumana con Justicia Social y en Paz.

        #YoVotoPetro
        #PetroPresidente
        HEX:50657266696c206f66696369616c2064656c206469726967656e746520706f6cc3ad7469636f2070726f677265736973746120436f6c6f6d6269616e6f204775737461766f20506574726f2e20506f7220756e612023436f6c6f6d62696148756d616e6120636f6e204a7573746963696120536f6369616c207920656e2050617a2e0a0a23596f566f746f506574726f200a23506574726f507265736964656e7465
        </description>
        <vertical canonical="nonprofit">
        Sin fines de lucro
        HEX:53696e2066696e6573206465206c7563726f
        </vertical>
        <website>
        https://petro.com.co
        HEX:68747470733a2f2f706574726f2e636f6d2e636f
        </website>
        <website>
        https://twitter.com/petrogustavo
        HEX:68747470733a2f2f747769747465722e636f6d2f706574726f6775737461766f
        </website>
        <business_hours timezone="America/Bogota">
        <business_hours_config mode="open_24h" day_of_week="sun">
        </business_hours_config>
        <business_hours_config mode="open_24h" day_of_week="mon">
        </business_hours_config>
        <business_hours_config mode="open_24h" day_of_week="tue">
        </business_hours_config>
        <business_hours_config mode="open_24h" day_of_week="wed">
        </business_hours_config>
        <business_hours_config mode="open_24h" day_of_week="thu">
        </business_hours_config>
        <business_hours_config mode="open_24h" day_of_week="fri">
        </business_hours_config>
        <business_hours_config mode="open_24h" day_of_week="sat">
        </business_hours_config>
        </business_hours>
        </profile>
        </notification>
    """
    def __init__(self, id,  _from, profile, timestamp, notify, offline, setJid, setId):
        super(BusinessNotificationProtocolEntity, self).__init__("business", _id, _from, timestamp, notify, offline)
        pass
