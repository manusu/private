package dbadaptor

import (
	"golang.org/x/net/context"
	"github.com/coreos/etcd/client"
    elock "github.com/Scalingo/go-etcd-lock"
    "log"
	"time"
)

type etcdDB struct{
    etcdcli *client.Client
    etcdurl []string
}


//In init,just test connect,then close
func initDB(path []string)dbInterface{
	cfg := client.Config{
		Endpoints:               Endpoints:   []string{"100.100.203.146:2379", "100.100.233.221:2379", "100.100.247.23:2379"},
		Transport:               client.DefaultTransport,
		// set timeout per request to fail fast when the target endpoint is unavailable
		HeaderTimeoutPerRequest: time.Second,
	}
	c, err := client.New(cfg)
	if err != nil {
		log.Fatal(err)
        return nil
	}
    return etcdDB{
        etcdcli:c,
        etcdurl:[]string{"100.100.203.146:2379", "100.100.233.221:2379", "100.100.247.23:2379"},
    }
}



func (dbcli etcdDB)OpenDB(){
    return 
}

func (dbcli etcdDB)closeDB(){
    return
}

func (dbcli etcdDB) WriteKey(key string,value interface{})error{
    kapi := client.NewKeysAPI(etcdDb.etcdcli)    
    //encodeValue,_ :gobEncode(value)

    resp, err := kapi.Set(context.Background(), key, values, nil)
	if err != nil {
		return err
	} else {
		// print common key info
		log.Printf("Set is done. Metadata is %q\n", resp)
	}
}

func (dbcli etcdDB) ReadKey(key string, to interface{}) error{
    kapi := client.NewKeysAPI(etcdDb.etcdcli)
	resp, err = kapi.Get(context.Background(), key, nil)
	if err != nil {
		return err
	} else {
		// print common key info
		log.Printf("Get is done. Metadata is %q\n", resp)
		// print value
		log.Printf("%q key has %q value\n", resp.Node.Key, resp.Node.Value)
	}
}


func addLock(cli *client.Client,lockname string)locker *elock.EtcdLocker{
    l, err := elock.Acquire(client, "/_ABCDEFGabc/fslock/"+lockname, 15)
    if lockErr, ok := err.(*elock.Error); ok {
        // Key already locked
        fmt.Println(lockErr)
        return l
    } else if err != nil {
        //Communication with etcd has failed or other error
        fmt.Println(err)
        return nil
    }
}

func releaseLock(l *elock.EtcdLocker){
    // It's ok, lock is granted for 60 secondes
    // When the opration is done we release the lock
    err = l.Release()
    if err != nil {
        // Something wrong can happen during release: connection problem with etcd
        fmt.Println(err)
    }
}




func main(){
	cli := initDB("localhost:9000")
	go func(){
		l :=addLock(cli.etcdcli,test)
		fmt.println("lock1")
		time.Sleep(time.Secone*20)
		releaseLock(l) 
	}()
		go func(){
		l :=addLock(cli.etcdcli,test)
		fmt.println("lock1")
		time.Sleep(time.Secone*5)
		releaseLock(l) 
	}()
	time.Sleep(time.Secone*30)
}
