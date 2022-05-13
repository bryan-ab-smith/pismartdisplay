# Ideas and To Dos

## Show current status of lights

tinytuya example of how to get light state:

```
    data = d.state()
    print('\nStatus of Bulb: %r and the Bulb is: ' % data)
    if (data['is_on']==True):
        print('ON')
    else:
        print('OFF')
```

#### Open Tasks

* [ ] How to get webpage to poll light status api?
* [ ] API endpoint to get status of a light.
