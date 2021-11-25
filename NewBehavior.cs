using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Constants
{
        public const int SQUARE_LENGTH = 5;
        public const float INITIAL_X = 168.6f-SQUARE_LENGTH/2;
        public const float INITIAL_Y = -54.69f;

        public const float INITIAL_Z = -120.5f+SQUARE_LENGTH/2;

        public const float WAIT_TIME = 0.05f;
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

public class NewBehavior : MonoBehaviour
{
    string simulationURL = null;
    private float timer = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
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
                Debug.Log("Connected to simulation through Web API");
                Debug.Log(simulationURL);
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
                MyCar cars = JsonUtility.FromJson<MyCar>(www.downloadHandler.text);
                Debug.Log(cars.ToString());

                float y = Constants.INITIAL_Y;
                float x = Constants.INITIAL_X + cars.x * Constants.SQUARE_LENGTH;
                float z = Constants.INITIAL_Z + cars.y * Constants.SQUARE_LENGTH;
                transform.position = new Vector3(x, y, z);
                transform.Rotate(new Vector3(0, cars.theta, 0));
            }
        }
    }

    // Update is called once per frame
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
