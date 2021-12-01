using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Constants
{
        public const float SQUARE_LENGTH = 4.98f;
        public const float INITIAL_X = 167;
        public const float INITIAL_Y = -54.69f;

        public const float INITIAL_Z = -117;

        public const float WAIT_TIME = 1.0f;
}

public static class JsonHelper
{
    public static T[] FromJson<T>(string json)
    {
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
        return wrapper.Items;
    }

    public static string ToJson<T>(T[] array)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper);
    }

    public static string ToJson<T>(T[] array, bool prettyPrint)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper, prettyPrint);
    }

    [System.Serializable]
    private class Wrapper<T>
    {
        public T[] Items;
    }
}

[System.Serializable]
class MyCar
{
    public float x;
    public float y;
    public int theta;

    override public string ToString()
    {
        return "X: " + x + ", Y: " + y + ", angulo: " + theta;
    }
}

public class BehaviorCars : MonoBehaviour
{
    public GameObject auto1;
    public GameObject auto2;
    public GameObject auto3;
    string simulationURL = null;
    private float timer = 0.0f;
    List<GameObject> carCollection;
    List<GameObject> carToChoose;
    void Start()
    {
        carCollection = new List<GameObject>();
        carToChoose = new List<GameObject>{auto1, auto2, auto3};
        StartCoroutine(ConnectToMesa());
    }

    IEnumerator ConnectToMesa()
    {
        WWWForm form = new WWWForm();

        using (UnityWebRequest www = UnityWebRequest.Post("http://localhost:5000/games", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                simulationURL = www.GetResponseHeader("Location");
                string data = www.GetResponseHeader("Items"); 
                int numItems;
                int.TryParse(data, out numItems);
                Debug.Log("Connected to simulation through Web API");
                Debug.Log(numItems);
                for(int i = 0; i < numItems; i++){
                    carCollection.Add(Instantiate(carToChoose[Random.Range(0, carToChoose.Count)], new Vector3(0,0,0), Quaternion.Euler(0,90,0)));
                }
            }
        }
    }

    IEnumerator UpdatePositions()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(simulationURL))
        {
            if (simulationURL != null)
            {
                // Request and wait for the desired page.
                yield return www.SendWebRequest();

                Debug.Log(www.downloadHandler.text);
                Debug.Log("Data has been processed");
                MyCar[] cars = JsonHelper.FromJson<MyCar>(www.downloadHandler.text);
                

                for(int i = 0; i < cars.Length; i++){
                    GameObject tmp = carCollection[i];
                    float y = Constants.INITIAL_Y;
                    float x = Constants.INITIAL_X + cars[i].x * Constants.SQUARE_LENGTH;
                    float z = Constants.INITIAL_Z + cars[i].y * Constants.SQUARE_LENGTH;
                    tmp.transform.position = new Vector3(x, y, z);
                    tmp.transform.Rotate(new Vector3(0, cars[i].theta, 0));
                }
            }
        }
    }


    void Update()
    {
        timer += Time.deltaTime;
        if (timer > Constants.WAIT_TIME)
        {
            StartCoroutine(UpdatePositions());
            timer = timer - Constants.WAIT_TIME;
        }
    }
}
