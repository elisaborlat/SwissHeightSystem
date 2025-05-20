import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;
import java.util.Locale;

import com.swisstopo.geodesy.htrans_lib.Header;
import com.swisstopo.geodesy.htrans_lib.Htrans;
import com.swisstopo.geodesy.reframe_lib.*;

public class App {
   
   public static void main(String[] args) throws Exception {
      System.out.println("Hello, World!");
      
      Reframe reframeObj = new Reframe();
      
      double[] PIL_6170 = new double[] {2540621.753,1181302.435,448.6834};
      
      try{
         double[] outputCoordinates = reframeObj.ComputeReframe(PIL_6170,
         IReframe.PlanimetricFrame.LV95,
         IReframe.PlanimetricFrame.LV95,
         IReframe.AltimetricFrame.LN02,
         IReframe.AltimetricFrame.LHN95);
         System.out.println(Arrays.toString(outputCoordinates));
      } catch (IllegalArgumentException e) {
         throw new RuntimeException(e);
      }
      
      // Read bin and write to Bougan ACSCII (xll and yll corner left down)
      Header m_Header = new Header();
      
      float[][] m_Bougan;

      DataInputStream in = null;

      File file = new File("norm-ln02.grd");
      InputStream inputStream = new FileInputStream(file);

      in = new DataInputStream(inputStream);
      m_Header.minY = ParseToDouble(in);
      m_Header.maxY = ParseToDouble(in);
      m_Header.minX = ParseToDouble(in);
      m_Header.maxX = ParseToDouble(in);
      m_Header.mesY = ParseToDouble(in);
      m_Header.mesX = ParseToDouble(in);
      m_Header.dimY = ParseToInteger(in);
      m_Header.dimX = ParseToInteger(in);
      m_Header.unit = in.readByte();
      m_Bougan = new float[m_Header.dimX][m_Header.dimY];
      
      for(int j = 0; j < m_Header.dimY; ++j) {
         for(int i = 0; i < m_Header.dimX; ++i) {
            m_Bougan[i][j] = ParseToSingle(in);
         }
      }
      

      BufferedWriter writer = null;
      
      try {
         writer = new BufferedWriter(new FileWriter("norm-ln02-ascii.grd"));
         
         // Write header information
         writer.write("ncols " + m_Header.dimY);
         writer.newLine();
         writer.write("nrows " + m_Header.dimX);
         writer.newLine();
         writer.write("xllcorner " + m_Header.minX);
         writer.newLine();
         writer.write("yllcorner " + m_Header.minY);
         writer.newLine();
         writer.write("cellsize " + m_Header.mesY); // Assuming square cells
         writer.newLine();
         writer.write("NODATA_value -9999");
         writer.newLine();
         
         // Write the grid data
         for (int j = 0; j < m_Header.dimX; ++j) {
            for (int i = 0; i < m_Header.dimY; ++i) {
               writer.write(String.format(Locale.US, "%.14f ", m_Bougan[j][i]));
            }
            writer.newLine(); // Move to the next row
         }
         
      } catch (IOException e) {
         e.printStackTrace();
      } finally {
         if (writer != null) {
            try {
               writer.close();
            } catch (IOException e) {
               e.printStackTrace();
            }
         }
      }
      
      Htrans _objHtrans = new Htrans();
      _objHtrans.ComputeHtrans(PIL_6170, false);
      
   }
   
   
   private static int ParseToInteger(DataInputStream in) {
      int[] value = new int[4];
      
      try {
         for(int j = 0; j < 4; ++j) {
            value[j] = in.readUnsignedByte();
         }
      } catch (Exception var4) {
         return -1;
      }
      
      return (value[3] & 255) << 24 | (value[2] & 255) << 16 | (value[1] & 255) << 8 | value[0] & 255;
   }
   
   private static float ParseToSingle(DataInputStream in) {
      byte[] value = new byte[4];
      
      try {
         for(int j = 0; j < 4; ++j) {
            value[j] = in.readByte();
         }
      } catch (Exception var3) {
         return -1.0F;
      }
      
      return ByteBuffer.wrap(value).order(ByteOrder.LITTLE_ENDIAN).getFloat();
   }
   
   private static double ParseToDouble(DataInputStream in) {
      int[] value = new int[8];
      
      try {
         for(int j = 0; j < 8; ++j) {
            value[j] = in.readUnsignedByte();
         }
      } catch (Exception var7) {
         return -1.0D;
      }
      
      double mantisse = (double)value[0] / Math.pow(16.0D, 13.0D) + (double)value[1] / Math.pow(16.0D, 11.0D) + (double)value[2] / Math.pow(16.0D, 9.0D) + (double)value[3] / Math.pow(16.0D, 7.0D) + (double)value[4] / Math.pow(16.0D, 5.0D) + (double)value[5] / Math.pow(16.0D, 3.0D) + (double)(value[6] % 16) / 16.0D;
      byte vorzeichen;
      if (value[7] > 128) {
         vorzeichen = -1;
      } else {
         vorzeichen = 1;
      }
      
      int exponent = value[7] % 128 * 16 + value[6] / 16 - 1023;
      return (double)vorzeichen * (1.0D + mantisse) * Math.pow(2.0D, (double)exponent);
   }
}
