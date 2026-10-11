// =============================================================================
//  Mundos Lejanos — coma y colas de cometa para cuerpos celestes (Kopernicus ya no permite partículas por .cfg)
//  Para cada nodo MUNDOSLEJANOS_COMETA { body = ... } dibuja en el espacio escalado (capa 10):
//    - una coma: halo verdoso que siempre mira a la cámara;
//    - una cola de iones: azul y recta, en dirección contraria a la estrella;
//    - una cola de polvo: blanco cálido, más ancha y curvada hacia atrás en la órbita.
//  La actividad crece al acercarse a la estrella (de activityStart a activityFull, en KAU): tamaño y brillo.
//  Compilar:  python herramientas/compilar_plugin.py  ->  GameData/MundosLejanos/Plugins/MundosLejanos.dll
// =============================================================================
using System;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

[assembly: KSPAssembly("MundosLejanos", 1, 0)]

namespace MundosLejanos
{
    [KSPAddon(KSPAddon.Startup.AllGameScenes, false)]
    public class Cometas : MonoBehaviour
    {
        const double KAU = 13599840256.0;
        readonly List<Cometa> cometas = new List<Cometa>();

        void Start()
        {
            if (FlightGlobals.Bodies == null || GameDatabase.Instance == null)
                return;
            foreach (ConfigNode node in GameDatabase.Instance.GetConfigNodes("MUNDOSLEJANOS_COMETA"))
            {
                CelestialBody body = FlightGlobals.Bodies.Find(b => b.bodyName == node.GetValue("body"));
                if (body == null || body.scaledBody == null)
                    continue;
                try
                {
                    cometas.Add(new Cometa(body, node));
                }
                catch (Exception e)
                {
                    Debug.LogError("[MundosLejanos] No se pudo crear el cometa " + body.bodyName + ": " + e);
                }
            }
            if (cometas.Count > 0)
                Debug.Log("[MundosLejanos] Cometas activos: " + cometas.Count);
        }

        void LateUpdate()
        {
            Camera cam = ScaledCamera.Instance != null ? ScaledCamera.Instance.cam : null;
            if (cam == null)
                return;
            foreach (Cometa c in cometas)
                c.Update(cam);
        }

        void OnDestroy()
        {
            foreach (Cometa c in cometas)
                c.Destroy();
            cometas.Clear();
        }

        static double Num(ConfigNode node, string key, double def)
        {
            double v;
            string s = node.GetValue(key);
            return s != null && double.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : def;
        }

        static Color Col(ConfigNode node, string key, Color def)
        {
            string s = node.GetValue(key);
            if (s == null)
                return def;
            string[] p = s.Split(',');
            if (p.Length < 3)
                return def;
            float[] f = new float[4] { 0, 0, 0, 1 };
            for (int i = 0; i < Math.Min(4, p.Length); i++)
                float.TryParse(p[i].Trim(), NumberStyles.Float, CultureInfo.InvariantCulture, out f[i]);
            return new Color(f[0], f[1], f[2], f[3]);
        }

        class Cometa
        {
            readonly CelestialBody body, star;
            readonly double activityStart, activityFull, comaRadius, ionLength, dustLength;
            readonly Color comaColor, ionColor, dustColor;
            readonly Pieza coma, ion, dust;

            public Cometa(CelestialBody body, ConfigNode node)
            {
                this.body = body;
                star = body.referenceBody;
                while (star != null && star.referenceBody != null && star.referenceBody != star && !star.isStar)
                    star = star.referenceBody;
                activityStart = Num(node, "activityStart", 40) * KAU;
                activityFull = Num(node, "activityFull", 4.2) * KAU;
                comaRadius = Num(node, "comaRadius", 4.0e7);
                ionLength = Num(node, "ionTailLength", 1.5e9);
                dustLength = Num(node, "dustTailLength", 8.0e8);
                comaColor = Col(node, "comaColor", new Color(0.70f, 0.95f, 0.80f, 1f));
                ionColor = Col(node, "ionTailColor", new Color(0.35f, 0.60f, 1.00f, 1f));
                dustColor = Col(node, "dustTailColor", new Color(1.00f, 0.88f, 0.70f, 1f));
                coma = new Pieza(body.bodyName + "_Coma", Quad(true), Texturas.Coma());
                ion = new Pieza(body.bodyName + "_ColaIones", Quad(false), Texturas.Cola(0.06f, 0.18f, 1.6f, true));
                dust = new Pieza(body.bodyName + "_ColaPolvo", Quad(false), Texturas.Cola(0.12f, 0.38f, 2.2f, false));
            }

            public void Update(Camera cam)
            {
                if (star == null)
                    return;
                Vector3d fromStar = body.position - star.position;
                double r = fromStar.magnitude;
                double t = Clamp01((activityStart - r) / (activityStart - activityFull));
                float a = (float)(t * t * (3 - 2 * t));
                bool on = a > 0.002f;
                coma.Show(on); ion.Show(on); dust.Show(on);
                if (!on)
                    return;

                float k = ScaledSpace.InverseScaleFactor;
                Vector3 head = body.scaledBody.transform.position;
                Vector3 anti = ((Vector3)fromStar).normalized;
                Vector3 vel = ((Vector3)body.orbit.GetWorldSpaceVel()).normalized;
                Vector3 dustDir = (anti - 0.45f * vel).normalized;              // el polvo se queda atrás en la órbita
                Vector3 toCam = cam.transform.position - head;

                float comaSize = (float)(2 * comaRadius * (0.3 + 0.7 * a)) * k;
                float inside = Mathf.Clamp01(toCam.magnitude / (0.6f * comaSize));   // dentro de la coma: casi no se ve
                coma.Place(head, Quaternion.LookRotation(-toCam.normalized, cam.transform.up), new Vector3(comaSize, comaSize, 1));
                coma.Tint(comaColor * (a * inside));

                float lenI = (float)(ionLength * a) * k, lenD = (float)(dustLength * a) * k;
                ion.Place(head, Billboard(anti, toCam), new Vector3(lenI * 0.25f, lenI, 1));
                ion.Tint(ionColor * (a * Mathf.Lerp(0.4f, 1f, inside)));
                dust.Place(head, Billboard(dustDir, toCam), new Vector3(lenD * 0.45f, lenD, 1));
                dust.Tint(dustColor * (0.8f * a * Mathf.Lerp(0.4f, 1f, inside)));
            }

            public void Destroy()
            {
                coma.Destroy(); ion.Destroy(); dust.Destroy();
            }

            // El eje Y del quad sigue la cola y su cara gira hacia la cámara alrededor de ese eje
            static Quaternion Billboard(Vector3 axis, Vector3 toCam)
            {
                Vector3 fwd = Vector3.ProjectOnPlane(toCam, axis);
                if (fwd.sqrMagnitude < 1e-6f)
                    fwd = Vector3.Cross(axis, Vector3.up);
                return Quaternion.LookRotation(-fwd.normalized, axis);
            }

            static double Clamp01(double x)
            {
                return x < 0 ? 0 : x > 1 ? 1 : x;
            }

            static Mesh Quad(bool centered)
            {
                float y0 = centered ? -0.5f : 0f, y1 = centered ? 0.5f : 1f;
                Mesh m = new Mesh();
                m.vertices = new[] { new Vector3(-0.5f, y0, 0), new Vector3(0.5f, y0, 0), new Vector3(0.5f, y1, 0), new Vector3(-0.5f, y1, 0) };
                m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(1, 1), new Vector2(0, 1) };
                m.triangles = new[] { 0, 2, 1, 0, 3, 2 };
                m.RecalculateBounds();
                m.bounds = new Bounds(Vector3.zero, Vector3.one * 4);          // sin recortes al escalar
                return m;
            }
        }

        // Una pieza visible: GameObject en la capa del espacio escalado con material aditivo
        class Pieza
        {
            readonly GameObject go;
            readonly MeshRenderer renderer;
            readonly Material material;

            public Pieza(string name, Mesh mesh, Texture2D tex)
            {
                go = new GameObject("MundosLejanos_" + name);
                go.layer = 10;
                go.AddComponent<MeshFilter>().sharedMesh = mesh;
                renderer = go.AddComponent<MeshRenderer>();
                Shader sh = Shader.Find("KSP/Particles/Additive") ?? Shader.Find("Legacy Shaders/Particles/Additive")
                            ?? Shader.Find("Particles/Additive");
                material = new Material(sh) { mainTexture = tex, renderQueue = 3100 };
                renderer.sharedMaterial = material;
                renderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
                renderer.receiveShadows = false;
            }

            public void Show(bool on)
            {
                if (renderer.enabled != on)
                    renderer.enabled = on;
            }

            public void Place(Vector3 pos, Quaternion rot, Vector3 scale)
            {
                go.transform.position = pos;
                go.transform.rotation = rot;
                go.transform.localScale = scale;
            }

            public void Tint(Color c)
            {
                c.a = 1f;
                if (material.HasProperty("_TintColor"))
                    material.SetColor("_TintColor", c * 0.5f);              // los shaders de partículas duplican el tinte
                if (material.HasProperty("_Color"))
                    material.color = c;
            }

            public void Destroy()
            {
                UnityEngine.Object.Destroy(material.mainTexture);
                UnityEngine.Object.Destroy(material);
                UnityEngine.Object.Destroy(go);
            }
        }

        // Texturas procedurales (no hace falta ningún archivo): RGB = A = intensidad
        static class Texturas
        {
            public static Texture2D Coma()
            {
                const int N = 128;
                Texture2D t = Nueva(N, N);
                for (int y = 0; y < N; y++)
                    for (int x = 0; x < N; x++)
                    {
                        float dx = (x + 0.5f) / N * 2 - 1, dy = (y + 0.5f) / N * 2 - 1;
                        float r2 = dx * dx + dy * dy;
                        float i = Mathf.Exp(-r2 / 0.02f) + 0.45f * Mathf.Exp(-r2 / 0.15f) + 0.15f * Mathf.Exp(-r2 / 0.5f);
                        i *= Mathf.Clamp01((1 - r2) * 4);                                     // sin borde cuadrado
                        t.SetPixel(x, y, Gris(Mathf.Clamp01(i)));
                    }
                t.Apply(true, true);
                return t;
            }

            // w0/w1: semiancho al principio y al final; fade: caída a lo largo; streaks: filamentos (cola de iones)
            public static Texture2D Cola(float w0, float w1, float fade, bool streaks)
            {
                const int W = 64, H = 256;
                Texture2D t = Nueva(W, H);
                for (int y = 0; y < H; y++)
                {
                    float v = (y + 0.5f) / H;
                    float w = Mathf.Lerp(w0, w1, v);
                    float along = Mathf.Pow(1 - v, fade) * Mathf.Clamp01(v * 40);           // nace junto a la coma
                    for (int x = 0; x < W; x++)
                    {
                        float u = (x + 0.5f) / W - 0.5f;
                        float i = Mathf.Exp(-(u * u) / (w * w)) * along;
                        if (streaks)
                            i *= 0.65f + 0.35f * Mathf.Sin(u * 90f + v * 7f) * Mathf.Sin(u * 37f - v * 3f);
                        t.SetPixel(x, y, Gris(Mathf.Clamp01(i)));
                    }
                }
                t.Apply(true, true);
                return t;
            }

            static Texture2D Nueva(int w, int h)
            {
                return new Texture2D(w, h, TextureFormat.RGBA32, true) { wrapMode = TextureWrapMode.Clamp, filterMode = FilterMode.Trilinear };
            }

            static Color Gris(float i)
            {
                return new Color(i, i, i, i);
            }
        }
    }
}
