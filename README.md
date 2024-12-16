# Cabigon's personal website

### Prerequisite
Install "Harp" library via node
```
npm install -g harp
```

### To deploy to github.io
After updating code in ejs, use harp to convert code to html format so that github.io can read.
```
harp _harp .
git add -A
git commit -m "message here"
git push origin master
```

### To local test
Use below command for local test, dafault listening port is at 9000, or use **--port** to define another port
```
harp _harp
harp --port 3001 _harp
```
